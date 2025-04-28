from time import sleep
from typing import List, Dict, Callable

from .device_mqtt import DeviceMqtt
from .device_serial import DeviceSerial
import logging


class DeviceElectricityAll(DeviceMqtt, DeviceSerial):
    def __init__(
            self,
            mqtt_publish: Callable[[DeviceMqtt, str, str], None],
            serial_send: Callable[[bytes], None],
    ):
        self.mqtt_publish = mqtt_publish
        self.serial_send = serial_send
        self.electricity_current = 0

    @property
    def device_id(self) -> str:
        return "electricity_all"

    @property
    def device_name(self) -> str:
        return "electricity_all"

    @property
    def device_tags(self) -> List[str]:
        return ["총 전기사용량"]

    @property
    def mqtt_device_type(self) -> str:
        return "sensor"

    def bytes_to_int(self, bytes):
        # 먼저, 바이트들을 하나씩 4비트 단위로 쪼갠다
        nibbles = []
        for byte in bytes:
            high = (byte >> 4) & 0x0F  # 상위 4비트
            low = byte & 0x0F  # 하위 4비트
            nibbles.append(high)
            nibbles.append(low)

        # 이제 nibbles 리스트를 숫자로 합치자
        result = 0
        for nibble in nibbles:
            result = result * 10 + nibble

        return result

    def receive_serial(self, data: bytes):
        if data.startswith(b'\xf7\x30\x03\x81\x08'):
            self.electricity_current = self.bytes_to_int(data[9:13])
            self.mqtt_publish(self, "state", self.electricity_current)

    @property
    def additional_payload(self) -> Dict[str, str]:
        return {
            "state_topic": "~/state",
            "optimistic": True
        }

    def receive_topic(self, topic: str, payload: str):
        return
        # if topic == "state-topic":
        #     if payload == "heat":
        #         self.turn_on()
        #     elif payload == "off":
        #         self.turn_off()
