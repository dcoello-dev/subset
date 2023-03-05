import os
import sys
import json
import argparse

import sources
import sinks
import storages

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
    help="add elem")

parser.add_argument(
    '-r', '--remove',
    action='store_true',
    help="remove elem")

parser.add_argument(
    '--reset',
    action='store_true',
    help="reset all elements")

parser.add_argument(
    '-s', '--select',
    action='store_true',
    help="select elem")

parser.add_argument(
    '-l', '--list',
    action='store_true',
    help="add elem")

parser.add_argument(
    '-i', '--index',
    type=int,
    default=-1,
    help="elem index")

parser.add_argument(
    '-d', '--domain',
    type=str,
    default="",
    help="elem domain")

parser.add_argument(
    '-v', '--value',
    type=str,
    default="",
    help="elem value")

args = parser.parse_args()

if __name__ == "__main__":
    config = json.loads(open(args.config, "r+").read())
    storage_t_ = REG_NAMESPACE[Type.STORAGE][config["storage"]]["instance"]
    DOMAIN = config["default_domain"] if args.domain == "" else args.domain
    VALUE = REG_NAMESPACE[Type.SOURCE][config["domains"][DOMAIN]["default_source"]]["instance"].get() \
        if args.value == "" else args.value

    if args.generate:
        storage_t_.create_storage(config, config["domains"])
        sys.exit(0)

    local = storage_t_(config)
    if args.add:
        local.add_elem_to_domain(DOMAIN, args.index, VALUE)

    if args.remove:
        local.remove_elem_from_domain(DOMAIN, args.index)

    if args.select:
        action, elem = local.select_elem_from_domain(DOMAIN, args.index)
        if elem["in_use"]:
            REG_NAMESPACE[Type.SINK][action]["instance"].send(elem["value"])

    if args.list:
        print(CLIFormat.format_domain(
            local.get_domain(DOMAIN)))

    if args.reset:
        local.reset_domain(DOMAIN)

    local.store_changes()
