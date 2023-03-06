import paho.mqtt.client as mqtt
from paho.mqtt import publish
import threading
import copy
import json


class MqttHandler(threading.Thread):
    """MqttHandler class implementation.
    Attributes:
        conf (dict): configuration parameters.
        connected (bool): flag connected.
        client (mqtt.Client): wrapped mqtt client.
        callback_ (func): callback function to call once a message arrives.
        buffer (list): buffer for sync mode.
    """

    def __init__(self,
                 conf=None,
                 callback=None):
        """CTOR.
        Args:
            conf (dict): kernel configuration parameters.
            callback (func): callback to call once a message is received.
        """
        threading.Thread.__init__(self)
        if conf is not None:
            self.conf = conf
            self.conf["timeout"] = 60
        else:
            self.conf = dict(host="localhost",
                             port=1883,
                             timeout=60,
                             subscribe=["subset/#"])
        self.connected = False
        self.client = mqtt.Client()
        self.callback_ = callback
        self.buffer = []

    def run(self):
        """Main function of the thread."""
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.conf["host"],
                            self.conf["port"],
                            self.conf["timeout"])
        for sub in self.conf["subscribe"]:
            self.client.subscribe(sub)
        self.client.loop_forever()

    def on_connect(self,
                   client,
                   userdata,
                   flags,
                   rc):
        """Callback on connect."""
        self.connected = True

    def on_message(self,
                   client,
                   userdata,
                   msg):
        """Callback on message."""
        try:
            payload = json.loads(msg.payload)
        except Exception:
            return
        message = dict(topic=msg.topic,
                       payload=payload)
        if self.callback_ is not None:
            self.callback_(message)
        else:
            self.buffer.append(message)

    def on_publish(self,
                   path,
                   payload,
                   host=None):
        """Sends message."""
        if host is not None:
            hst_ = host
        else:
            hst_ = self.conf["host"]
        publish.single(path,
                       payload,
                       hostname=hst_,
                       retain=True)

    def get_buffer(self):
        """Returns stored buffer."""
        toret = copy.deepcopy(self.buffer)
        self.buffer = []
        return toret

    def stop(self):
        """Stops the iface."""
        self.client.disconnect()
        self.connected = False
