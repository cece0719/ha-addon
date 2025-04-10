from time import sleep
from typing import List, Dict, Callable

from .device_mqtt import DeviceMqtt
from .device_serial import DeviceSerial
import logging


class DeviceBoiler(DeviceMqtt, DeviceSerial):
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
        self.set_temperature = 30
        self.current_temperatrue = 15
        self.mqtt_publish = mqtt_publish
        self.serial_send = serial_send

    @property
    def device_id(self) -> str:
        return "boiler_{}".format(self.number)

    @property
    def device_name(self) -> str:
        return self.__device_name

    @property
    def device_tags(self) -> List[str]:
        return self.__device_tags

    @property
    def mqtt_device_type(self) -> str:
        return "climate"

    def turn_on(self):
        self.serial_send(b'\x36' + (self.number + 16).to_bytes(1, "big") + b'\x43\x01\x01')

    def turn_off(self):
        self.serial_send(b'\x36' + (self.number + 16).to_bytes(1, "big") + b'\x43\x01\x00')

    def receive_serial(self, data: bytes):
        if data.startswith(b'\xf7\x36\x1f\x81'):
            status = data[6] & (1<<(self.number-1)) != 0
            set_temperature = data[8+(self.number*2)]
            current_temperature = data[9+(self.number*2)]
            if status:
                self.mqtt_publish(self, "state", "heat")
            else:
                self.mqtt_publish(self, "state", "off")
            self.mqtt_publish(self, "set_temperature", str(set_temperature))
            self.mqtt_publish(self, "current_temperature", str(current_temperature))

    @property
    def additional_payload(self) -> Dict[str, str]:
        return {
            "mode_state_topic": "~/state",
            "mode_command_topic": "~/command",
            "temperature_state_topic": "~/set_temperature",
            "current_temperature_topic": "~/current_temperature",
            "temperature_command_topic": "~/set",
            "modes" : ["off", "heat"],
            "temperature_unit" : "C",
        }

    def receive_topic(self, topic: str, payload: str):
        if topic == "command":
            if payload == "heat":
                self.turn_on()
            elif payload == "off":
                self.turn_off()
        elif topic == "set":
            while True:
                set_temperature: int = int(float(payload))
                self.serial_send(b'\x36' + (self.number + 16).to_bytes(1, "big") + b'\x44\x01' + (set_temperature & 0xFF).to_bytes(1, 'big'))
                if set_temperature == self.set_temperature :
                    break
                sleep(0.3)
