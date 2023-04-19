from collections import defaultdict


class Type:
    SINK = "sink"
    SOURCE = "source"
    STORAGE = "storage"
    PROXY = "proxy"
    KEYLOGGER = "keylogger"


REG_NAMESPACE = defaultdict(dict)


def Register(type_reg: str, name: str, description: str):
    """Register implementation.

    Args:
        name (Type): type of registered entity.
        name (str): implementation id.
        description (str): implementation description.
        short (str, optional): short argparse val. Defaults to None.
        long (str, optional): long argparse val. Defaults to None.
    """
    def wrapper(cls):
        REG_NAMESPACE[type_reg][name] = dict(instance=(cls),
                                             description=description)
        return cls
    return wrapper
