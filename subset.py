import os
import json
import argparse

import sources
import sinks
import storages
import proxys
import keyloggers

from core.Register import *
from core.Controller import Controller
from front.TUIFront import TUIFront

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

parser.add_argument(
    '--keylogger',
    action='store_true',
    help="keylogger")

parser.add_argument(
    '--tui',
    action='store_true',
    help="tui")

args = parser.parse_args()

if __name__ == "__main__":
    file = open(args.config, "r+")
    config = json.loads(file.read())
    file.close()

    storage_t_ = REG_NAMESPACE[Type.STORAGE][config["storage"]
                                             ["type"]]["instance"]
    proxy_t_ = REG_NAMESPACE[Type.PROXY][config["proxy"]["type"]]["instance"]

    DOMAIN = config["default_domain"] if args.domain == "" else args.domain

    USER = config["user"] if args.user == "" else args.user

    if args.generate:
        storage_t_.create_storage(config, config["domains"])

        local = storage_t_(config["storage"])
        proxy = proxy_t_(config["proxy"])

        for domain in config["domains"].keys():
            if config["domains"][domain]["shared"]:
                proxy.update_shared_domain(
                    config["user"], domain, local.get_domain(domain))

    local = storage_t_(config["storage"])
    proxy = proxy_t_(config["proxy"])
    controller = Controller(config, REG_NAMESPACE, proxy, local)

    if args.tui:
        tui = TUIFront(config, REG_NAMESPACE, local)
        if args.keylogger:
            key = REG_NAMESPACE[Type.KEYLOGGER][config["default_keylogger"]]["instance"](
                config, REG_NAMESPACE, controller)
            key.start()
        tui.run()

    if args.keylogger:
        key = REG_NAMESPACE[Type.KEYLOGGER][config["default_keylogger"]]["instance"](
            config, REG_NAMESPACE, controller)
        key.run()

    VALUE, sch = REG_NAMESPACE[Type.SOURCE][config["domains"]
                                            [DOMAIN]["default_source"]]["instance"]().get()

    if args.add:
        controller.add(DOMAIN, args.index, VALUE)

    if args.remove:
        controller.remove(DOMAIN, args.index)

    if args.select:
        controller.select(USER, DOMAIN, args.index)

    if args.list:
        controller.show(USER, DOMAIN, sch)

    if args.reset:
        controller.reset(DOMAIN)

    controller.__del__()
