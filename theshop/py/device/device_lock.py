from typing import List, Dict, Callable

from .device_clova import DeviceClova
from .device_mqtt import DeviceMqtt


class DeviceLock(DeviceMqtt, DeviceClova):
    def __init__(
            self,
            mqtt_publish: Callable[[DeviceMqtt, str, str], None],
            serial_send: Callable[[bytes], None],
    ):
        self.mqtt_publish = mqtt_publish
        self.serial_send = serial_send

    @property
    def device_id(self) -> str:
        return "btn_door"

    @property
    def device_name(self) -> str:
        return "문"

    @property
    def device_tags(self) -> List[str]:
        return ["문"]

    def open(self):
        self.serial_send(b'\x40\x03\x22\x00')

    @property
    def additional_payload(self) -> Dict[str, str]:
        return {
            "command_topic": "~/command",
            "state_topic": "~/state",
            "payload_lock": "LOCK",
            "payload_unlock": "UNLOCK",
            "state_locked": "LOCK",
            "state_unlocked": "UNLOCK"
        }

    def receive_topic(self, topic: str, payload: str):
        if topic == "command":
            if payload == "UNLOCK":
                self.open()

    def receive_serial(self, data: bytes):
        if data.startswith(b'\xf7\x40\x03\x01\x00'):
            self.mqtt_publish(self, "state", "LOCK")

    @property
    def mqtt_device_type(self) -> str:
        return "lock"

    @property
    def appliance_types(self) -> list[str]:
        return ["SMARTLOCK"]

    @property
    def clova_actions(self) -> list[str]:
        return ["SetLockState"]

    def action(self, body) -> Dict:
        if body["header"]["name"] == "SetLockStateRequest" and body["payload"]["lockState"] == "UNLOCKED":
            self.open()
        ret = {
            "header": body["header"],
            "payload": {
                "lockState": body["payload"]["lockState"]
            }
        }
        ret["header"]["name"] = "SetLockStateConfirmation"
        return ret
