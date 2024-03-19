from typing import List, Dict

from device_mqtt import DeviceMqtt
from device_serial import DeviceSerial
from theshopmqtt import TheShopMQTT
from theshopserial import TheShopSerial


class DeviceLightTotal(DeviceMqtt, DeviceSerial):
    def __init__(
            self,
            mqtt: TheShopMQTT,
            serial: TheShopSerial
    ):
        self.mqtt = mqtt
        self.serial = serial
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
        self.serial.send(b'\x33\x01\x41\x01\x00')

    def turn_off(self):
        self.serial.send(b'\x33\x01\x41\x01\x01')

    def receive_serial(self, data: bytes):
        if data.startswith(b'\xf7\x33\x01\x81'):
            self.status = (data[6] != 4)
            self.mqtt.publish(self, "state", "ON")

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
