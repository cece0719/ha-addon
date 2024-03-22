from typing import List, Dict, Callable
from device_mqtt import DeviceMqtt


class DeviceElevator(DeviceMqtt):
    def __init__(
            self,
            serial_send: Callable[[bytes], None],
    ):
        self.serial_send = serial_send

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
        self.serial_send(b'\x33\x01\x81\x03\x00\x20\x00')

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
