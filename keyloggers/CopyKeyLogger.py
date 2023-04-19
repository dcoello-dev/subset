import time
import pyperclip
from pynput import keyboard

from keyloggers.KeyLogger import KeyLogger
from core.Register import Type, Register


@Register(Type.KEYLOGGER, "copy_kl",
          "Keylogger that wraps copy hotkeys")
class CopyKeyLogger(KeyLogger):
    def __init__(self, conf: dict, namespace, controller):
        super().__init__(conf, namespace, controller)

        self._domain = "clip"
        self._user = self._conf["user"]
        self._action = None
        self._last = ""

    def on_activate_copy(self):
        time.sleep(0.1)
        value = pyperclip.paste()
        if self._last != value and value != "":
            self._last = value
            self._controller.add(
                self._domain,
                0,
                dict(str=value))

    def on_selection(self, idx):
        self._controller.select(self._user, self._domain, idx)

    def __decorate(self, idx, fnc):
        def inner():
            return fnc(idx)
        return inner

    def capture(self):
        dispatcher = {'<ctrl>+c': self.on_activate_copy,
                      '<ctrl>+<shift>+c': self.on_activate_copy}
        dispatcher.update(
            {'<ctrl>+' + str(i): self.__decorate(i, self.on_selection)
             for i in range(0, 10)}
        )
        with keyboard.GlobalHotKeys(dispatcher) as h:
            h.join()
