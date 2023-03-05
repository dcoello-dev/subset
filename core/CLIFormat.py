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
    def colored(str: str, color: str) -> str:
        return color + str + CLIFormat.ENDC

    @staticmethod
    def format_domain(domain: dict) -> str:
        msg = ""
        for elem in domain["elems"]:
            if elem["in_use"]:
                msg += CLIFormat.colored(str(elem["id"]),
                                         CLIFormat.OKGREEN + CLIFormat.BOLD)
                msg += ": "
                msg += elem["value"][:40]
                msg += "\n"
        return msg
