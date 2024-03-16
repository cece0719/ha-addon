import paho.mqtt.client as paho_mqtt
import json
import time
import logging


class TheShopMQTT:
    def __init__(self):
        self.devices = []

        self.mqtt_prefix = "cece0719"
        self.is_connect = False
        self.mqtt = paho_mqtt.Client()

    def add_device(self, device):
        self.devices.append(device)

    def on_connect(self, mqtt, userdata, flags, rc):
        self.is_connect = True

        self.mqtt.subscribe("{}/#".format(self.mqtt_prefix), 0)
        for device in self.devices:
            if hasattr(device, "publishes"):
                for publish in device.publishes:
                    topic = publish["topic"]
                    payload = publish["payload"]
                    payload["device"] = {
                        "ids": ["cece0719", ],
                        "name": "cec0e719",
                        "mf": "Samsung SDS",
                        "mdl": "Samsung SDS Wallpad",
                        "sw": "n-andflash/ha_addons/sds_wallpad",
                    }
                    self.mqtt.publish(topic, json.dumps(payload))

        logging.info("mqtt on connect success")

    def on_disconnect(self, mqtt, userdata, rc):
        logging.info("mqtt disconnected!!")
        self.is_connect = False

    def on_message(self, mqtt, userdata, msg):
        logging.info("get messaged {}".format(msg.topic))
        logging.info("get payload {}".format(msg.payload.decode()))
        for device in self.devices:
            device.receive_mqtt(msg.topic, msg.payload.decode())

    def start(self):
        self.mqtt.on_connect = (lambda mqtt, userdata, flags, rc: self.on_connect(mqtt, userdata, flags, rc))
        self.mqtt.on_disconnect = (lambda mqtt, userdata, rc: self.on_disconnect(mqtt, userdata, rc))
        self.mqtt.on_message = (lambda mqtt, userdata, msg: self.on_message(mqtt, userdata, msg))
        self.mqtt.username_pw_set("xxx", "xxx")
        self.mqtt.connect("192.168.10.150")
        self.mqtt.loop_start()

        while not self.is_connect:
            logging.info("waiting MQTT connected ...")
            time.sleep(1)

        logging.info("mqtt connect success!!")
