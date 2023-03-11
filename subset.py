import os
import sys
import time
import json
import argparse

import sources
import sinks
import storages
import proxys

from core.Register import *
from core.CLIFormat import CLIFormat

parser = argparse.ArgumentParser()

parser.add_argument(
    '-c', '--config',
    default=os.path.expanduser('~') + "/.config/subset/config",
    help="configuration file")

parser.add_argument(
    '-gen', '--generate',
    action='store_true',
    help="generate storage")

parser.add_argument(
    '-a', '--add',
    action='store_true',
    help="add elem to domain")

parser.add_argument(
    '-r', '--remove',
    action='store_true',
    help="remove elem from domain")

parser.add_argument(
    '--reset',
    action='store_true',
    help="reset all elements")

parser.add_argument(
    '-s', '--select',
    action='store_true',
    help="select elem from domain")

parser.add_argument(
    '-l', '--list',
    action='store_true',
    help="list domain elementas")

parser.add_argument(
    '-i', '--index',
    type=int,
    default=-1,
    help="elem index")

parser.add_argument(
    '-d', '--domain',
    type=str,
    default="",
    help="domain, by default it is taken from configuration file")

parser.add_argument(
    '-u', '--user',
    type=str,
    default="",
    help="user")

args = parser.parse_args()

if __name__ == "__main__":
    config = json.loads(open(args.config, "r+").read())

    storage_t_ = REG_NAMESPACE[Type.STORAGE][config["storage"]
                                             ["type"]]["instance"]
    proxy_t_ = REG_NAMESPACE[Type.PROXY][config["proxy"]["type"]]["instance"]

    DOMAIN = config["default_domain"] if args.domain == "" else args.domain

    VALUE, sch = REG_NAMESPACE[Type.SOURCE][config["domains"]
                                            [DOMAIN]["default_source"]]["instance"]().get()

    USER = config["user"] if args.user == "" else args.user

    proxy = proxy_t_(config["proxy"])

    if args.generate:
        storage_t_.create_storage(config, config["domains"])
        local = storage_t_(config["storage"])
        for domain in config["domains"].keys():
            if config["domains"][domain]["shared"]:
                proxy.update_shared_domain(
                    USER, domain, local.get_domain(domain))

    local = storage_t_(config["storage"])

    if args.add:
        local.add_elem_to_domain(DOMAIN, args.index, VALUE)
        if config["domains"][DOMAIN]["shared"]:
            _, elem = local.select_elem_from_domain(DOMAIN, args.index)
            proxy.update_shared_domain_elem(USER, DOMAIN, args.index, elem)

    if args.remove:
        local.remove_elem_from_domain(DOMAIN, args.index)
        if config["domains"][DOMAIN]["shared"]:
            _, elem = local.select_elem_from_domain(DOMAIN, args.index)
            proxy.update_shared_domain_elem(USER, DOMAIN, args.index, elem)

    if args.select:
        action, elem = local.select_elem_from_domain(DOMAIN, args.index)
        if elem["in_use"]:
            REG_NAMESPACE[Type.SINK][action]["instance"]().send(elem["value"])

    if args.list:
        if USER == config["user"]:
            print(CLIFormat.format_domain(USER, DOMAIN,
                                          local.get_domain(DOMAIN), sch))
        else:
            print(CLIFormat.format_domain(USER, DOMAIN,
                                          proxy.get_shared_domain(USER, DOMAIN), sch))

    if args.reset:
        local.reset_domain(DOMAIN)
        if config["domains"][DOMAIN]["shared"]:
            proxy.update_shared_domain(USER, DOMAIN, local.get_domain(DOMAIN))

    local.store_changes()
    time.sleep(0.1)
    proxy.__del__()
