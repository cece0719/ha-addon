from typing import List, Dict

import serial
import logging
import threading
from functools import reduce

from device.device import Device
from device.device_serial import DeviceSerial


def bytes_xor(in_bytes):
    return reduce(lambda acc, cur: acc ^ cur, in_bytes, 0).to_bytes(1)


def bytes_sum(in_bytes):
    return reduce(lambda acc, cur: (acc + cur) & 255, in_bytes, 0).to_bytes(1)


class TheShopSerial:
    def __init__(
            self,
            option
    ):
        self.option = option
        self.request_command = []
        self.devices: Dict[str, DeviceSerial] = {}

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

    def add_devices(self, devices: List[Device]):
        for device in devices:
            if isinstance(device, DeviceSerial):
                self.devices[device.device_id] = device

    def read_raw(self):
        while True:
            header = self._ser.read(1)
            if header == b'\xf7':
                break
            logging.info("header is not f7 try again : {}".format(str(header.hex())))

        device_id = self._ser.read(1)
        device_sub_id = self._ser.read(1)
        command_type = self._ser.read(1)
        length = self._ser.read(1)
        data = self._ser.read(int.from_bytes(length))
        xor_sum = self._ser.read(1)
        add_sum = self._ser.read(1)

        return header + device_id + device_sub_id + command_type + length + data + xor_sum + add_sum

    def send(self, command):
        command = b'\xf7' + command
        command = command + bytes_xor(command)
        command = command + bytes_sum(command)
        logging.info("append command : {}".format(command.hex(" ")))
        self.request_command.append(command)

    def start(self):
        def listen():
            while True:
                data = self.read_raw()
                logging.debug(data.hex(" "))
                for device in self.devices.values():
                    device.receive_serial(data)

                if len(self.request_command) > 0 and data[3] == 129:
                    command = self.request_command.pop()
                    logging.info("write command  : {}".format(command.hex(" ")))
                    self._ser.write(command)

        threading.Thread(target=listen).start()
