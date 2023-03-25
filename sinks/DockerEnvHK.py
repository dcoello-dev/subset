import os
from string import Template

from core.Register import Type, Register
from pynput.keyboard import Controller, Key


from sinks.Sink import Sink
from interfaces.SimpleString import SimpleString


@Register(Type.SINK, "enter_env_hk", "Enter docker dev env")
class DockerEnvHK(Sink):
    def __init__(self):
        super().__init__([SimpleString])
        self._cmd = Template("""docker run --rm -it --security-opt apparmor=unconfined --cap-add=sys_nice \
--user "$UID:$GID" \
--volume="/etc/group:/etc/group:ro" \
-e "HOME=/home/$USER" \
-e "DISPLAY=$DISPLAY" \
--pid=host \
--volume="/tmp/.X11-unix:/tmp/.X11-unix" \
--volume="/home/$USER:/home/$USER" \
--volume="/etc/passwd:/etc/passwd:ro" \
--volume="/etc/shadow:/etc/shadow:ro" \
--volume="${workdir}:/opt/workspace" \
--network host ${image} /bin/bash """)

    def send_sink(self, data: dict) -> None:
        keyboard = Controller()
        keyboard.type(self._cmd.safe_substitute(
            dict(
                image=data["str"],
                workdir=os.getcwd())))
        keyboard.tap(Key.enter)
        keyboard.tap(Key.enter)
