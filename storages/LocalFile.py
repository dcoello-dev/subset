import json
import os

from core.Register import Register, Type
from storages.Storage import Storage


@Register(Type.STORAGE, "local_file", "Store buffers on json file")
class LocalStorage(Storage):
    def __init__(self, config: dict):
        super().__init__(config)
        self._update_data()
        self._policy_dispatcher = dict(
            BY_INDEX=self._policy_by_index,
            FIFO=self._policy_fifo)

    def _policy_by_index(self, domain, index, value):
        if domain in self._storage.keys():
            for elem in self._storage[domain]["elems"]:

                if index == -1 and not elem["in_use"] and value != "":
                    elem["value"] = value
                    elem["in_use"] = True
                    break

                if elem["id"] == index and value != "":
                    elem["value"] = value
                    elem["in_use"] = True
                    break

    def _policy_fifo(self, domain, _, value):
        if domain in self._storage.keys():
            l = len(self._storage[domain]["elems"])
            for i in range(1, l):
                self._storage[domain]["elems"][l -
                                               i]["value"] = self._storage[domain]["elems"][l -
                                                                                            i -
                                                                                            1]["value"]
                if self._storage[domain]["elems"][l - i]["value"] != "":
                    self._storage[domain]["elems"][l - i]["in_use"] = True
            self._storage[domain]["elems"][0]["value"] = value
            if value != "":
                self._storage[domain]["elems"][0]["in_use"] = True

    def _update_data(self):
        file_ = open(self._config["file"], "r")
        self._storage = json.loads(file_.read())
        file_.close()
        self.last_updated_ = os.path.getmtime(self._config["file"])

    def store_changes(self) -> None:
        file_ = open(self._config["file"], "w+")
        file_.write(json.dumps(self._storage, indent=2))
        file_.close()
        self.last_updated_ = os.path.getmtime(self._config["file"])

    def check_updates(self) -> bool:
        return self.last_updated_ != os.path.getmtime(self._config["file"])

    @staticmethod
    def create_storage(config: dict, domains: list) -> None:
        file_ = open(config["storage"]["file"], "w+")
        to_store_ = {"meta":
                     {
                         "user": config["user"]
                     }
                     }

        for domain, cfg in domains.items():
            to_store_[domain] = {
                "buffer_size": cfg["buffer_size"],
                "policy": cfg["policy"],
                "default_sink": cfg["default_sink"],
                "default_source": cfg["default_source"],
                "elems": [{"id": i, "in_use": False, "value": ""} for i in range(0, cfg["buffer_size"])]
            }

        file_.write(json.dumps(to_store_, indent=2))

    def get_domain(self, domain: str) -> dict:
        if self.check_updates():
            self._update_data()
        return self._storage[domain]

    def get_domains(self) -> list:
        if self.check_updates():
            self._update_data()
        return [k for k in self._storage.keys() if k != "meta"]

    def get_list(self, domain: str) -> list:
        if self.check_updates():
            self._update_data()
        return self._storage[domain]["elems"]

    def reset_domain(self, domain: str):
        if domain in self._storage.keys():
            for elem in self._storage[domain]["elems"]:
                elem["value"] = ""
                elem["in_use"] = False

    def add_elem_to_domain(self, domain: str, index: int, value) -> None:
        if self.check_updates():
            self._update_data()
        self._policy_dispatcher[self._storage[domain]["policy"]](
            domain, index, value)
        self.store_changes()

    def remove_elem_from_domain(self, domain: str, index: int) -> None:
        if domain in self._storage.keys():
            for elem in self._storage[domain]["elems"]:
                if elem["id"] == index:
                    elem["value"] = ""
                    elem["in_use"] = False
                    break

    def select_elem_from_domain(self, domain: str, index: int) -> None:
        if self.check_updates():
            self._update_data()
        if domain in self._storage.keys():
            for elem in self._storage[domain]["elems"]:
                if elem["id"] == index:
                    return self._storage[domain]["default_sink"], elem
