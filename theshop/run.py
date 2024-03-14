import serial
import paho.mqtt.client as paho_mqtt
import json

import sys
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os.path
import re

logger = logging.getLogger(__name__)


class KSX4506_Serial:
    def __init__(self):
        self._ser = serial.Serial()
        self._ser.port = "/dev/ttyUSB0"
        self._ser.baudrate = 9600
        self._ser.bytesize = 8
        self._ser.parity = "N"
        self._ser.stopbits = 1

        self._ser.close()
        self._ser.open()

        self._ser.timeout = None

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

        data_bytes = header
        data_bytes += device_id
        data_bytes += device_sub_id
        data_bytes += command_type
        data_bytes += length
        data_bytes += data
        data_bytes += xor_sum
        data_bytes += add_sum

        return data_bytes

    def send(self, a):
        self._ser.write(a)


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
    dump_loop(KSX4506_Serial())