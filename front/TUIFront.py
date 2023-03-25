import pytermgui as ptg

from pytermgui import Label, Splitter, Button, Collapsible, Container

from core.Register import *
from core.CLIFormat import CLIFormat


class TUIFront:
    def __init__(self, conf, namespace, storage):
        self._conf = conf
        self._namespace = namespace
        self._storage = storage

        self._main = Label("main", parent_align=0)

    def __callback(self, bt):
        sch = self._namespace[Type.SOURCE][self._conf["domains"]
                                           [bt.label]["default_source"]]["instance"]().get_schema()
        self._main.value = CLIFormat.format_domain(self._conf["user"], bt.label,
                                                   self._storage.get_domain(bt.label), sch)

    def run(self):
        with ptg.WindowManager() as manager:
            elems = [Button(dom, centered=True, relative_width=0.7, onclick=self.__callback)
                     for dom in self._storage.get_domains()]

            manager.layout.add_slot(name="domains", width=0.2)
            manager.layout.add_slot(name="main", width=0.8)
            manager.add(
                ptg.Window(
                    Container(
                        Collapsible("DOMAINS", *elems, keyboard=True,
                                    vertical_align=2, relative_height=0.9), vertical_align=2, relative_height=0.9),
                ), assign="domains", animate=False
            )

            manager.add(
                ptg.Window(
                    Container(
                        self._main, vertical_align=1),
                ), assign="main", animate=True
            )
