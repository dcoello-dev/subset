import os
import sys
import json
import argparse
import pyperclip


class LocalStorage:
    def __init__(self, config):
        self._config = config
        file_ = open(config["file"], "r")
        self._storage = json.loads(file_.read())
        file_.close()

    def store_changes(self):
        file_ = open(self._config["file"], "w+")
        file_.write(json.dumps(self._storage, indent=2))
        file_.close()

    @staticmethod
    def create_storage(config, domains):
        file_ = open(config["file"], "w+")
        to_store_ = {"meta":
                     {
                         "user": config["user"]
                     }
                     }

        for domain, N, action in domains:
            to_store_[domain] = {
                "max_elems": N,
                "default_action": action,
                "elems": [{"id": i, "in_use": False, "value": ""} for i in range(0, N)]
            }

        file_.write(json.dumps(to_store_, indent=2))

    def get_domain(self, domain):
        return self._storage[domain]

    def get_list(self, domain):
        return self._storage[domain]["elems"]

    def add_elem_to_domain(self, domain, index, value):
        if domain in self._storage.keys():
            for elem in self._storage[domain]["elems"]:

                if index == -1 and not elem["in_use"]:
                    elem["value"] = value
                    elem["in_use"] = True
                    break

                if elem["id"] == index:
                    elem["value"] = value
                    elem["in_use"] = True
                    break

    def remove_elem_from_domain(self, domain, index):
        if domain in self._storage.keys():
            for elem in self._storage[domain]["elems"]:
                if elem["id"] == index:
                    elem["value"] = ""
                    elem["in_use"] = False
                    break

    def select_elem_from_domain(self, domain, index):
        if domain in self._storage.keys():
            for elem in self._storage[domain]["elems"]:
                if elem["id"] == index:
                    return self._storage[domain]["default_action"], elem


class CLIFormat:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def colored(str, color):
        return color + str + CLIFormat.ENDC

    @staticmethod
    def format_domain(domain):
        msg = ""
        for elem in domain["elems"]:
            if elem["in_use"]:
                msg += CLIFormat.colored(str(elem["id"]),
                                         CLIFormat.OKGREEN + CLIFormat.BOLD)
                msg += ": "
                msg += elem["value"][:40]
                msg += "\n"
        return msg


parser = argparse.ArgumentParser()

parser.add_argument(
    '-c', '--config',
    default=os.path.expanduser('~') + "/.config/.subset/config",
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
    help="elem value")

args = parser.parse_args()

ACTIONS = {
    "clip": pyperclip.copy
}

if __name__ == "__main__":
    config = json.loads(open(args.config, "r+").read())

    DOMAIN = config["default_domain"] if args.domain == "" else args.domain

    if args.generate:
        LocalStorage.create_storage(config, config["domains"])
        sys.exit(0)

    local = LocalStorage(config)
    if args.add:
        local.add_elem_to_domain(DOMAIN, args.index, args.value)

    if args.remove:
        local.remove_elem_from_domain(DOMAIN, args.index)

    if args.select:
        action, elem = local.select_elem_from_domain(DOMAIN, args.index)
        if elem["in_use"]:
            ACTIONS[action](elem["value"])

    if args.list:
        print(CLIFormat.format_domain(local.get_domain("clip")))

    local.store_changes()
