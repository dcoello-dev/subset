from pynput.keyboard import Controller, Key
from string import Template

from core.Register import Type, Register

from sinks.Sink import Sink
from interfaces.GitLocation import GitLocation


@Register(Type.SINK, "goto_checkout_hk",
          "Go to directory and checkout to branch")
class GotoCheckoutHK(Sink):
    def __init__(self):
        super().__init__([GitLocation])
        self._cmd = Template("cd ${dir} && git checkout ${branch}")

    def send_sink(self, data: dict) -> None:
        cmd = self._cmd.safe_substitute(data)
        keyboard = Controller()
        keyboard.type(cmd)
        keyboard.tap(Key.enter)
        keyboard.tap(Key.enter)
