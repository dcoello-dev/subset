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
    def format_domain(user: str, domain_id: str, domain: dict, sch) -> str:
        msg = CLIFormat.colored("user: ",
                                CLIFormat.WARNING) + CLIFormat.colored(user,
                                                                       CLIFormat.OKGREEN) + "\n"
        msg += CLIFormat.colored("domain: ",
                                 CLIFormat.WARNING) + CLIFormat.colored(domain_id,
                                                                        CLIFormat.OKGREEN) + "\n"
        for elem in domain["elems"]:
            if elem["in_use"]:
                msg += CLIFormat.colored(str(elem["id"]),
                                         CLIFormat.OKGREEN) + ": "
                msg += sch().to_string(elem["value"]) + "\n"
        return msg
