import time

from core.Observer import Subject, Observer
from core.Register import Type
from core.CLIFormat import CLIFormat


class Controller(Subject):
    def __init__(self, conf: dict, namespace, proxy, storage):
        self._conf = conf
        self._proxy = proxy
        self._storage = storage
        self._namespace = namespace
        self._observers = []

    def __del__(self):
        self._storage.store_changes()
        time.sleep(0.1)
        self._proxy.__del__()

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        self._observers.remove(observer)

    def notify(self, event: dict) -> None:
        """
        Notify all observers about an event.
        """
        map(lambda e: e.update(self, e), self._observers)

    def add(self, domain: str, index: int, value: dict):
        print("ADD")
        self._storage.add_elem_to_domain(domain, index, value)
        if self._conf["domains"][domain]["shared"]:
            _, elem = self._storage.select_elem_from_domain(domain, index)
            self._proxy.update_shared_domain_elem(self._conf["user"],
                                                  domain, index, elem)
        self.notify(dict(event="add"))

    def remove(self, domain: str, index: int):
        self._storage.remove_elem_from_domain(domain, index)
        if self._conf["domains"][domain]["shared"]:
            _, elem = self._storage.select_elem_from_domain(domain, index)
            self._proxy.update_shared_domain_elem(
                self._conf["user"], domain, index, elem)

    def select(self, user: str, domain: str, index: int):
        if user == self._conf["user"]:
            action, elem = self._storage.select_elem_from_domain(domain, index)
        else:
            shared_domain = self._proxy.get_shared_domain(user, domain)
            elem = {}
            for e in shared_domain:
                if e["id"] == index:
                    elem = e
        if elem != {} and elem["in_use"]:
            self._namespace[Type.SINK][action]["instance"]().send(
                elem["value"])

    def show(self, user: str, domain: str, iface):
        if user == self._conf["user"]:
            print(CLIFormat.format_domain(user, domain,
                                          self._storage.get_domain(domain), iface))
        else:
            print(CLIFormat.format_domain(user, domain,
                                          self._proxy.get_shared_domain(user, domain), iface))

    def reset(self, domain: str):
        self._storage.reset_domain(domain)
        if self._conf["domains"][domain]["shared"]:
            self._proxy.update_shared_domain(
                self._conf["user"], domain, self._storage.get_domain(domain))
