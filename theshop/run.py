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

logger = logging.getLogger(__name__)

class KSX4506_Serial:
    def __init__(self):
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
            logger.info("header is not f7 try again : " + str(header.hex()))

        device_id = self._ser.read(1)
        device_sub_id = self._ser.read(1)
        command_type = self._ser.read(1)
        length = self._ser.read(1)
        data = self._ser.read(int.from_bytes(length))
        xor_sum = self._ser.read(1)
        add_sum = self._ser.read(1)

        return header+device_id+device_sub_id+command_type+length+data+xor_sum+add_sum

    def send(self, a):
        self._ser.write(a)

    def start(self):
        while True:
            data = self.read_raw()
            logger.info(data.hex(" "))


class TheShopMQTT:
    def __init__(self):
        self.is_connect = False
        self.mqtt = paho_mqtt.Client()

    def on_connect(self, mqtt, userdata, flags, rc):
        self.is_connect = True

        topic = "homeassistant/button/test/button1/config"
        logger.info("mqtt subscribe!")
        self.mqtt.subscribe("#", 0)
        logger.info("mqtt publish!")
        self.mqtt.publish(topic, json.dumps({
            "unique_id": "button_1",
            "name": "button_1_1",
            "command_topic": "cece0719/button1/command"
        }))
        logger.info("mqtt on connect success")

    def on_disconnect(self, mqtt, userdata, rc):
        self.is_connect = False

    def on_message(self, mqtt, userdata, msg):
        logger.info("get messaged {}".format(msg))
        logger.info("get messaged {}".format(userdata))

    def start(self):
        self.mqtt.on_connect = (lambda mqtt, userdata, flags, rc: self.on_connect(mqtt, userdata, flags, rc))
        self.mqtt.on_disconnect = (lambda mqtt, userdata, rc: self.on_disconnect(mqtt, userdata, rc))
        self.mqtt.on_message = (lambda mqtt, userdata, msg: self.on_disconnect(mqtt, userdata, msg))
        self.mqtt.username_pw_set("xxx", "xxx")
        self.mqtt.connect("192.168.10.150")
        self.mqtt.loop_start()

        while not self.is_connect:
            logger.info("waiting MQTT connected ...")
            time.sleep(1)

        logger.info("mqtt connect success!!")


def init_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def dump_loop(ksx4506_serial):
    logger.info("dump start")
    while True:
        data = ksx4506_serial.read_raw()
        logger.info(data.hex(" "))


if __name__ == "__main__":
    init_logger()
    logger.info("initialize serial...")
    mqtt = TheShopMQTT()
    mqtt.start()
    serial = KSX4506_Serial()
    serial.start()