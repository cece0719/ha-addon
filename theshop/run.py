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

        self._ser.timeout = 0.0

        while True:
            data=self._ser.read(1)
            if data:
                continue
            else:
                break

        self._ser.timeout = None

    def readRaw(self):
        while True:
            header = self.read(1)
            if header == b'\xf7':
                break
            logger.info("header is not f7 try again : " + " {:02X}".format(header))

        deviceId = self._ser.read(1)
        deviceSubId = self._ser.read(1)
        commandType = self._ser.read(1)
        length = self._ser.read(1)
        data = self._ser.read(int.from_bytes(length, "little"))
        xorSum = self._ser.read(1)
        addSum = self._ser.read(1)

        bytes = header
        bytes += deviceId
        bytes += deviceSubId
        bytes += commandType
        bytes += length
        bytes += data
        bytes += xorSum
        bytes += addSum

        return bytes

    def send(self, a):
        self._ser.write(a)


def init_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def dump_loop():
    logger.info("dump start")
    while True:
        data = conn.readRaw()

        if data:
            logs = []
            for b in data:
                logs.append(" {:02X}".format(b))
            logger.info("".join(logs))


if __name__ == "__main__":
    global conn

    # configuration 로드 및 로거 설정
    init_logger()

    logger.info("initialize serial...")
    conn = KSX4506_Serial()

    dump_loop()