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


class SDSSerial:
    def __init__(self):
        self._ser = serial.Serial()
        self._ser.port = "/dev/ttyUSB0"
        self._ser.baudrate = 9600
        self._ser.bytesize = 8
        self._ser.parity = "N"
        self._ser.stopbits = 1

        self._ser.close()
        self._ser.open()

        self._pending_recv = 0

        # 시리얼에 뭐가 떠다니는지 확인
        self.set_timeout(5.0)
        data = self._recv_raw(1)
        self.set_timeout(None)
        if not data:
            logger.critical("no active packet at this serial port!")

    def _recv_raw(self, count=1):
        return self._ser.read(count)

    def recv(self, count=1):
        # serial은 pending count만 업데이트
        self._pending_recv = max(self._pending_recv - count, 0)
        return self._recv_raw(count)

    def send(self, a):
        self._ser.write(a)

    def set_pending_recv(self):
        self._pending_recv = self._ser.in_waiting

    def check_pending_recv(self):
        return self._pending_recv

    def check_in_waiting(self):
        return self._ser.in_waiting

    def set_timeout(self, a):
        self._ser.timeout = a


def init_logger():
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%H:%M:%S")
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def dump_loop():
    conn.set_timeout(0.0)
    logs = []
    while True:
        try:
            data = conn.recv(conn.check_in_waiting())
        except:
            continue

        if data:
            logs = []
            for b in data:
                #               if b == 0xA1 or len(logs) > 500:
                #                   logger.info("".join(logs))
                #                   logs = ["{:02X}".format(b)]
                #               elif b <= 0xA0: logs.append(   "{:02X}".format(b))
                #               elif b == 0xFF: logs.append(   "{:02X}".format(b))
                #               elif b == 0xB0: logs.append( ": {:02X}".format(b))
                #               else:           logs.append(",  {:02X}".format(b))
                logs.append(" {:02X}".format(b))
            logger.info("".join(logs))
        time.sleep(0.01)

    logger.info("".join(logs))
    logger.warning("dump done.")
    conn.set_timeout(None)


if __name__ == "__main__":
    global conn

    # configuration 로드 및 로거 설정
    init_logger()

    logger.info("initialize serial...")
    conn = SDSSerial()

    dump_loop()