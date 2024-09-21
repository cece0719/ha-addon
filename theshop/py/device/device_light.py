from typing import List, Dict, Callable

from .device_clova import DeviceClova
from .device_mqtt import DeviceMqtt
from .device_serial import DeviceSerial
import logging


class DeviceLight(DeviceMqtt, DeviceSerial, DeviceClova):
    def __init__(
            self,
            number: int,
            device_name: str,
            device_tags: List[str],
            mqtt_publish: Callable[[DeviceMqtt, str, str], None],
            serial_send: Callable[[bytes], None],
    ):
        self.number = number
        self.__device_name = device_name
        self.__device_tags = device_tags
        self.status = False
        self.mqtt_publish = mqtt_publish
        self.serial_send = serial_send

    @property
    def device_id(self) -> str:
        return "light_{}".format(self.number)

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
        self.serial_send(b'\x0E' + (self.number + 16).to_bytes(1, "big") + b'\x41\x01\x01')

    def turn_off(self):
        self.serial_send(b'\x0E' + (self.number + 16).to_bytes(1, "big") + b'\x41\x01\x00')

    def receive_serial(self, data: bytes):
        if data.startswith(b'\xf7\x0e\x1f\x81'):
            if data[5 + self.number] == 1:
                logging.debug("light" + str(self.number) + "status on")
                self.mqtt_publish(self, "state", "ON")
                self.status = True
            else:
                logging.debug("light" + str(self.number) + "status off")
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

    @property
    def appliance_types(self) -> list[str]:
        return ["LIGHT"]

    @property
    def clova_actions(self) -> list[str]:
        return ["TurnOn", "TurnOff"]

    def action(self, body) -> Dict:
        ret = {
            "header": body["header"],
            "payload": {}
        }

        if body["header"]["name"] == "TurnOnRequest":
            self.turn_on()
            ret["header"]["name"] = "TurnOnConfirmation"
        elif body["header"]["name"] == "TurnOffRequest":
            self.turn_off()
            ret["header"]["name"] = "TurnOffConfirmation"

        return ret