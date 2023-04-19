import time
from pynput import keyboard

from keyloggers.KeyLogger import KeyLogger
from core.Register import Type, Register


@Register(Type.KEYLOGGER, "generic_kl",
          "Generic Keylogger")
class GenericKeyLogger(KeyLogger):
    def __init__(self, conf: dict, namespace, controller):
        super().__init__(conf, namespace, controller)

        self._domain = self._conf["default_domain"]
        self._user = self._conf["user"]
        self._indexes = "0123456789"
        self._simbols = "=!\"·$%&/()"
        self._dispatcher = {
            "l": self.__show,
            self._indexes: self.__select,
            self._simbols: self.__add
        }

        self._action = None

    @staticmethod
    def __kts(key) -> str:
        return str(key).replace("\'", "")

    def __show(self, _):
        sch = self._namespace[Type.SOURCE][self._conf["domains"]
                                           [self._domain]["default_source"]]["instance"]().get_schema()
        self._controller.show(self._user, self._domain, sch)

    def __select(self, key):
        self._controller.select(self._user, self._domain, int(key))

    def __add(self, key):
        value, _ = self._namespace[Type.SOURCE][self._conf["domains"]
                                                [self._domain]["default_source"]]["instance"]().get()
        self._controller.add(
            self._user,
            self._domain,
            self._simbols.find(key),
            value)

    def set_domain(self, domain: str) -> None:
        self._domain = domain

    def on_press(self, key):
        for k, v in self._dispatcher.items():
            if self.__kts(key) in k:
                self._action = (v, self.__kts(key))

    def on_activate_domain(self):
        with keyboard.Listener(on_press=self.on_press,
                               on_release=None,
                               suppress=True) as listener:
            time.sleep(self._conf["keylogger"]["command_delay"])
            listener.stop()

        if self._action is not None:
            self._action[0](self._action[1])
            self._action = None

    def capture(self):
        with keyboard.GlobalHotKeys({
                self._conf["keylogger"]["activation_hk"]: self.on_activate_domain}) as h:
            h.join()
