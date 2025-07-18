from typing import List, Dict, Callable

from .device_mqtt import DeviceMqtt
from .device_serial import DeviceSerial
import logging


class DeviceLight(DeviceMqtt, DeviceSerial):
    def __init__(
            self,
            number: int,
            sub_number: int,
            device_name: str,
            device_tags: List[str],
            mqtt_publish: Callable[[DeviceMqtt, str, str], None],
            serial_send: Callable[[bytes], None],
    ):
        self.number = number
        self.sub_number = sub_number
        self.__device_name = device_name
        self.__device_tags = device_tags
        self.status = False
        self.mqtt_publish = mqtt_publish
        self.serial_send = serial_send

    @property
    def device_id(self) -> str:
        return "light_{}_{}".format(self.number, self.sub_number)

    @property
    def device_name(self) -> str:
        return self.__device_name

    @property
    def device_tags(self) -> List[str]:
        return self.__device_tags

    @property
    def mqtt_device_type(self) -> str:
        return "light"

    def turn_on(self):
        self.serial_send(b'\x0E' + (self.number + 16).to_bytes(1, "big") + b'\x41\x03' + self.sub_number.to_bytes(1, "big") + b'\x01\x00')

    def turn_off(self):
        self.serial_send(b'\x0E' + (self.number + 16).to_bytes(1, "big") + b'\x41\x03' + self.sub_number.to_bytes(1, "big") + b'\x00\x00')

    def receive_serial(self, data: bytes):
        if data.startswith(b'\xf7\x0e' + (self.number + 16).to_bytes(1, "big") + b'\x81'):

            #가끔 잘못된 데이터 들어오는 걸로 보여 추가
            if len(data) <= (5 + self.sub_number):
                return

            if data[5 + self.sub_number] == 1:
                logging.debug("light{} status on".format(str(self.number)))
                self.mqtt_publish(self, "state", "ON")
                self.status = True
            else:
                logging.debug("light{} status off".format(str(self.number)))
                self.mqtt_publish(self, "state", "OFF")
                self.status = False

    @property
    def additional_payload(self) -> Dict[str, str]:
        return {
            "command_topic": "~/command",
            "state_topic": "~/state",
            "payload_on": 'ON',
            "payload_off": 'OFF',
        }

    def receive_topic(self, topic: str, payload: str):
        if topic == "command":
            if payload == "ON":
                self.turn_on()
            elif payload == "OFF":
                self.turn_off()

