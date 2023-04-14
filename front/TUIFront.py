import time
import threading
import pytermgui as ptg

from pytermgui import Label, Splitter, Button, Collapsible, Container

from core.Register import *
from core.CLIFormat import CLIFormat


class AutoUpdater(threading.Thread):
    def __init__(self, storage, front):
        threading.Thread.__init__(self)
        self._stop = False
        self._storage = storage
        self._front = front

    def stop(self):
        self._stop = True

    def run(self):
        try:
            while not self._stop:
                if self._storage.check_updates():
                    self._front._update_main()
                time.sleep(0.1)
        except Exception:
            pass


class TUIFront:
    def __init__(self, conf, namespace, storage):
        self._conf = conf
        self._namespace = namespace
        self._storage = storage

        self._local_user = self._conf["user"]
        self._actual_user = self._conf["user"]
        self._actual_domain = self._conf["default_domain"]
        self._build_header()

        self._selected_comains = []
        self._main = Label("", parent_align=0)

        self._auto_updater = AutoUpdater(self._storage, self)
        self._auto_updater.start()

    def __del__(self):
        self._auto_updater.stop()

    def _update_main(self):
        msg = ""

        for domain in self._selected_comains:
            msg += CLIFormat.colored(domain.upper(),
                                     CLIFormat.BOLD + CLIFormat.OKBLUE) + "\n"
            sch = self._namespace[Type.SOURCE][self._conf["domains"]
                                               [domain]["default_source"]]["instance"]().get_schema()

            buttons = []
            for elem in self._storage.get_domain(domain)["elems"]:
                if elem["in_use"]:
                    msg += CLIFormat.colored(str(elem["id"]),
                                             CLIFormat.BOLD + CLIFormat.OKGREEN) + "-> "
                    msg += sch().to_string(elem["value"])
                    msg += "\n"
                    buttons.append(
                        Button(
                            msg,
                            centered=True,
                            relative_width=0.7))
            msg += "\n"
        self._main.value = msg

    def __callback(self, bt):
        if bt.label not in self._selected_comains:
            self._selected_comains.append(bt.label)
        else:
            self._selected_comains.remove(bt.label)

        self._update_main()

    def _build_header(self) -> Label:
        self._header = Label(self._local_user + " " +
                             self._actual_user + " " +
                             self._actual_domain, parent_align=2)

    def _define_layout(self, manager):
        manager.layout.add_slot("header", height=0.1)
        manager.layout.add_break()
        manager.layout.add_slot(name="domains", width=0.2)
        manager.layout.add_slot(name="main", width=0.8)
        manager.layout.add_break()

    def run(self):
        with ptg.WindowManager() as manager:
            elems = [Button(dom, centered=True, relative_width=0.7, onclick=self.__callback)
                     for dom in self._storage.get_domains()]

            self._define_layout(manager)

            manager.add(
                ptg.Window(self._header,
                           ), assign="header", animate=False
            )

            manager.add(
                ptg.Window(
                    self._main,
                    vertical_align=ptg.VerticalAlignment.TOP
                ), assign="main", animate=True
            )

            lateral_window = ptg.Window(
                Collapsible("DOMAINS", *elems, keyboard=True),
                Label(""),
                Collapsible("REMOTES", *elems, keyboard=True),
                vertical_align=ptg.VerticalAlignment.TOP,
            )
            manager.add(
                lateral_window, assign="domains", animate=False
            )
