import serial
import logging
from functools import reduce


def bytes_xor(in_bytes):
    return reduce(lambda acc, cur: acc ^ cur, in_bytes, 0).to_bytes(1)


def bytes_sum(in_bytes):
    return reduce(lambda acc, cur: (acc + cur) & 255, in_bytes, 0).to_bytes(1)


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

    def add_device(self, device):
        self.devices.append(device)

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
