import threading
from abc import ABC, abstractmethod


class KeyLogger(threading.Thread):
    def __init__(self, conf: dict, namespace, controller):
        threading.Thread.__init__(self)
        self._conf = conf

        self._namespace = namespace
        self._controller = controller

    @abstractmethod
    def capture() -> None:
        pass

    def run(self):
        self.capture()
