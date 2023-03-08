import fcntl
import shlex
import termios
from pathlib import Path

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
    BACKSPACE = '\x08'

    @staticmethod
    def colored(str: str, color: str) -> str:
        return color + str + CLIFormat.ENDC

    @staticmethod
    def write_on_parent_shell(cmd: str, NB: int = 0):
        backspace = CLIFormat.BACKSPACE * NB
        cmd = f"{backspace}{cmd}\n"
        for c in cmd:
            fcntl.ioctl(2, termios.TIOCSTI, c)

    @staticmethod
    def format_domain(domain: dict) -> str:
        msg = ""
        for elem in domain["elems"]:
            if elem["in_use"]:
                msg += CLIFormat.colored(str(elem["id"]),
                                         CLIFormat.OKGREEN + CLIFormat.BOLD)
                msg += ": "
                if type(elem["value"]) is str:
                    msg += elem["value"][:40]
                else:
                    for k, v in elem["value"].items():
                        msg += CLIFormat.colored(k, CLIFormat.WARNING + CLIFormat.BOLD) + ": "
                        msg += CLIFormat.colored(v + " ", CLIFormat.OKBLUE)
                    msg = msg[:-2]
                msg += "\n"
        return msg
