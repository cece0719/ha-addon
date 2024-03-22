from typing import List, Dict, Callable

from device_mqtt import DeviceMqtt
from device_serial import DeviceSerial
from device import Device


class DeviceLightTotal(DeviceMqtt, DeviceSerial):
    def __init__(
            self,
            mqtt_publish: Callable[[Device, str, str], None],
            serial_send: Callable[[bytes], None],
    ):
        self.mqtt_publish = mqtt_publish
        self.serial_send = serial_send
        self.status = False

    @property
    def device_id(self) -> str:
        return "light_total"

    @property
    def device_name(self) -> str:
        return "소등"

    @property
    def device_tags(self) -> List[str]:
        return []

    @property
    def mqtt_device_type(self) -> str:
        return "light"

    def turn_on(self):
        self.serial_send(b'\x33\x01\x41\x01\x00')

    def turn_off(self):
        self.serial_send(b'\x33\x01\x41\x01\x01')

    def receive_serial(self, data: bytes):
        if data.startswith(b'\xf7\x33\x01\x81'):
            self.status = (data[6] != 4)
            if self.status:
                self.mqtt_publish(self, "state", "ON")
            else:
                self.mqtt_publish(self, "state", "OFF")

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
