from typing import List, Dict

from device_mqtt import DeviceMqtt
from theshopmqtt import TheShopMQTT
from theshopserial import TheShopSerial


class DeviceElevator(DeviceMqtt):
    def __init__(
            self,
            mqtt: TheShopMQTT,
            serial: TheShopSerial
    ):
        self.mqtt = mqtt
        self.serial = serial

    @property
    def device_id(self) -> str:
        return "btn_elevator"

    @property
    def device_name(self) -> str:
        return "엘리베이터"

    @property
    def device_tags(self) -> List[str]:
        return []

    def call(self):
        self.serial.send(b'\x33\x01\x81\x03\x00\x20\x00')

    @property
    def additional_payload(self) -> Dict[str, str]:
        return {
            "command_topic": "~/command",
        }

    def receive_topic(self, topic: str, payload: str):
        if topic == "command":
            if payload == "PRESS":
                self.call()

    @property
    def mqtt_device_type(self) -> str:
        return "button"
