import json
import time
from collections import defaultdict

from core.Register import Type, Register
from core.MQTTHandler import MqttHandler

from proxys.Proxy import Proxy


@Register(Type.PROXY, "mqtt_retain",
          "Global namespace built on top of MQTT protocol")
class MQTTRetain(Proxy):

    ROOT = "subset"

    def __init__(self, config: dict):
        super().__init__(config)
        self._handler = MqttHandler(conf=self._config)
        self._handler.start()
        self._buffer = []

    def __del__(self):
        self._handler.stop()

    def _bp(self, elems: list):
        return "/".join([self.ROOT] + elems)

    def load_elems(self):
        if len(self._buffer) == 0:
            for _ in range(0, 10):
                self._buffer = self._handler.get_buffer()
                if len(self._buffer) > 0:
                    break
                else:
                    time.sleep(0.1)

    def update_shared_domain(
            self, user: str, domain: str, storage: dict) -> None:
        meta = dict(buffer_size=storage["buffer_size"],
                    default_sink=storage["default_sink"],
                    default_source=storage["default_source"])
        self._handler.on_publish(self._bp([user, domain]), json.dumps(meta))

        for elem in storage["elems"]:
            self._handler.on_publish(
                self._bp([user, domain, str(elem["id"])]), json.dumps(elem))

    def update_shared_domain_elem(
            self, user: str, domain: str, index: int, data: dict):
        self._handler.on_publish(
            self._bp([user, domain, str(index)]), json.dumps(data))

    def list_shared_domains(self):
        ret = defaultdict(dict)
        self.load_elems()
        for elem in self._buffer:
            u_domain = elem["topic"].split("/")
            if len(u_domain) == 3:
                ret[u_domain[1]][u_domain[2]] = elem["payload"]

        return ret

    def get_shared_domain(self, user: str, domain: str):
        ret = dict()
        ret["elems"] = []
        self.load_elems()
        for elem in self._buffer:
            u_domain = elem["topic"].split("/")
            if u_domain[1] == user and u_domain[2] == domain:
                if len(u_domain) == 4:
                    ret["elems"].append(elem["payload"])
                if len(u_domain) == 3:
                    ret.update(elem["payload"])
        return ret
