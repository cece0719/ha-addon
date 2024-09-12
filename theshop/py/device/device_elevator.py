from typing import List, Dict, Callable

from .device_clova import DeviceClova
from .device_mqtt import DeviceMqtt


class DeviceElevator(DeviceMqtt, DeviceClova):
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

    def call_elevator(self):
        self.serial_send(b'\x33\x01\x81\x03\x00\x20\x00')

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

    @property
    def appliance_types(self) -> list[str]:
        return ["BUILDING_ELEVATOR_CALLER"]

    @property
    def clova_actions(self) -> list[str]:
        return ["CallElevator"]

    def action(self, body) -> Dict:
        self.call_elevator()
        ret = {
            "header": body["header"],
            "payload": {}
        }
        ret["header"]["name"] = "CallElevatorConfirmation"
        return ret
