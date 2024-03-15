from functools import reduce

import serial
import paho.mqtt.client as paho_mqtt
import json
#
# import sys
import time
import logging
# from logging.handlers import TimedRotatingFileHandler
# import os.path
# import re


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt="%H:%M:%S")


def bytes_xor(bytes):
    return reduce(lambda acc, cur: acc ^ cur, bytes, 0).to_bytes(1)


def bytes_sum(bytes):
    return reduce(lambda acc, cur: (acc + cur) & 255, bytes, 0).to_bytes(1)


class TheShopSerial:
    def __init__(self):
        self.request_command = []
        self.devices = []

        self._ser = serial.Serial()
        self._ser.port = "/dev/ttyUSB0"
        self._ser.baudrate = 9600
        self._ser.bytesize = 8
        self._ser.parity = "N"
        self._ser.stopbits = 1
        self._ser.timeout = None

        self._ser.close()
        self._ser.open()

        self._ser.reset_input_buffer()
        self._ser.reset_output_buffer()

    def read_raw(self):
        while True:
            header = self._ser.read(1)
            if header == b'\xf7':
                break
            logging.info("header is not f7 try again : " + str(header.hex()))

        device_id = self._ser.read(1)
        device_sub_id = self._ser.read(1)
        command_type = self._ser.read(1)
        length = self._ser.read(1)
        data = self._ser.read(int.from_bytes(length))
        xor_sum = self._ser.read(1)
        add_sum = self._ser.read(1)

        return header+device_id+device_sub_id+command_type+length+data+xor_sum+add_sum

    def send(self, command):
        logging.info("request command : " + command.hex(" "))
        self.request_command.append(command)

    def start(self):
        while True:
            data = self.read_raw()
            logging.info(data.hex(" "))
            for device in self.devices:
                device.receive_serial(data)

            if len(self.request_command) > 0:
                logging.info("write command")
                command = self.request_command.pop()
                logging.info("command : " + command.hex(" "))
                self._ser.write(command)


class TheShopMQTT:
    def __init__(self):
        self.devices = []

        self.mqtt_prefix = "cece0719"
        self.is_connect = False
        self.mqtt = paho_mqtt.Client()

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
            device.receive_serial(msg.topic, msg.payload.decode)

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


def dump_loop(ksx4506_serial):
    logging.info("dump start")
    while True:
        data = ksx4506_serial.read_raw()
        logging.info(data.hex(" "))


if __name__ == "__main__":
    logging.info("initialize serial...")

    serial = TheShopSerial()
    serial.start()
    mqtt = TheShopMQTT()
    mqtt.start()