from typing import List, Dict, Callable

from .device_mqtt import DeviceMqtt
from .device_light_total import DeviceLightTotal


class DeviceElevator(DeviceMqtt):
    def __init__(
            self,
            device_light_total: DeviceLightTotal,
            serial_send: Callable[[bytes], None],
    ):
        self.device_light_total = device_light_total
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

    def call_elevator(self):
        if self.device_light_total.status :
            self.serial_send(b'\x33\x01\x81\x03\x00\x20\x00')
        else :
            self.serial_send(b'\x33\x01\x81\x03\x00\x24\x00')

    @property
    def additional_payload(self) -> Dict[str, str]:
        return {
            "command_topic": "~/command",
        }

    def receive_topic(self, topic: str, payload: str):
        if topic == "command":
            if payload == "PRESS":
                self.call_elevator()

    @property
    def mqtt_device_type(self) -> str:
        return "button"


