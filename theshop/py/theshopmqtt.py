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

        topic = "homeassistant/scene/sds_wallpad/scene_1/config"

        logging.info("subscribe : " + "{}/#".format(self.mqtt_prefix))
        self.mqtt.subscribe("{}/#".format(self.mqtt_prefix), 0)
        self.mqtt.publish(topic, json.dumps({
            "unique_id": "scene_1_1",
            "command_topic": "{}/scene_1/command".format(self.mqtt_prefix),
            "payload_on": 'daaad',
            "device": {
                "ids": ["sds_wallpad",],
                "name": "sds_wallpad",
                "mf": "Samsung SDS",
                "mdl": "Samsung SDS Wallpad",
                "sw": "n-andflash/ha_addons/sds_wallpad",
            }
        }))

        topic = "homeassistant/button/sds_wallpad/button_1/config"
        self.mqtt.publish(topic, json.dumps({
            "unique_id": "button_1",
            "command_topic": "{}/button_1/command".format(self.mqtt_prefix),
            "payload_on": 'daaad',
            "object_id": "button1_o",
            "name": "button1_n",
            "device": {
                "ids": ["sds_wallpad",],
                "name": "sds_wallpad",
                "mf": "Samsung SDS",
                "mdl": "Samsung SDS Wallpad",
                "sw": "n-andflash/ha_addons/sds_wallpad",
            }
        }))

        topic = "homeassistant/switch/sds_wallpad/switch_1/config"
        self.mqtt.publish(topic, json.dumps({
            "unique_id": "switch_1u",
            "command_topic": "{}/switch_1/command".format(self.mqtt_prefix),
            "object_id": "switch_1o",
            "name": "switch_1n",
            "device": {
                "ids": ["sds_wallpad",],
                "name": "sds_wallpad",
                "mf": "Samsung SDS",
                "mdl": "Samsung SDS Wallpad",
                "sw": "n-andflash/ha_addons/sds_wallpad",
            }
        }))

        topic = "homeassistant/button/sds_wallpad/button_9/config"
        self.mqtt.publish(topic, json.dumps({
            "unique_id": "button_9u",
            "command_topic": "{}/button_9c/command".format(self.mqtt_prefix),
            "object_id": "mqtt_button_2",
            "name": "button_9n",
            "device": {
                "ids": ["sds_wallpad",],
                "name": "sds_wallpad",
                "mf": "Samsung SDS",
                "mdl": "Samsung SDS Wallpad",
                "sw": "n-andflash/ha_addons/sds_wallpad",
            }
        }))

        logging.info("mqtt on connect success")

    def on_disconnect(self, mqtt, userdata, rc):
        logging.info("mqtt disconnected!!")
        self.is_connect = False

    def on_message(self, mqtt, userdata, msg):
        logging.info("get messaged {}".format(msg.topic))
        logging.info("get payload {}".format(msg.payload.decode()))
        for device in self.devices:
            device.receive_mqtt(msg.topic, msg.payload.decode)

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
