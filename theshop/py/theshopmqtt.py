from typing import List, Dict

import paho.mqtt.client as paho_mqtt
import json
import time
import logging

from device.device import Device
from device.device_mqtt import DeviceMqtt


class TheShopMQTT:
    def __init__(self):
        self.devices: Dict[str, DeviceMqtt] = {}

        self.mqtt_prefix = "cece0719"
        self.is_connect = False
        self.mqtt = paho_mqtt.Client()

    def add_devices(self, devices: List[Device]):
        for device in devices:
            if isinstance(device, DeviceMqtt):
                self.devices[device.device_id] = device

    def on_connect(self, mqtt, userdata, flags, rc):
        self.is_connect = True
        self.mqtt.subscribe("{}/#".format(self.mqtt_prefix), 0)
        for device in self.devices.values():
            topic = "homeassistant/{}/{}/{}/config".format(device.mqtt_device_type, self.mqtt_prefix, device.device_id)
            payload = {
                "unique_id": device.device_id,
                "name": device.device_name,
                "~": "{}/{}".format(self.mqtt_prefix, device.device_id),
            }
            payload.update(device.additional_payload)
            payload["device"] = {
                "ids": ["cece0719 the shop"],
                "name": "cece0719 the shop",
                "mf": "cece0719 mf",
                "mdl": "cece0719 the shop mdl",
                "sw": "cece0719/ha_addons/the_shop",
            }
            self.mqtt.publish(topic, json.dumps(payload))
        logging.info("mqtt on connect success")

    def on_disconnect(self, mqtt, userdata, rc):
        logging.info("mqtt disconnected!!")
        self.is_connect = False

    def on_message(self, mqtt, userdata, msg):
        logging.info("get messaged {}".format(msg.topic))
        logging.info("get payload {}".format(msg.payload.decode()))
        topic: str = msg.topic
        topics = topic.split("/")
        device_id = topics[1]
        device = self.devices[device_id]
        payload = msg.payload.decode()

        device.receive_topic("/".join(topics[2:]), payload)

    def publish(self, device: DeviceMqtt, topic: str, payload: str) -> None:
        self.mqtt.publish("{}/{}/{}".format(self.mqtt_prefix, device.device_id, topic), payload)

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
