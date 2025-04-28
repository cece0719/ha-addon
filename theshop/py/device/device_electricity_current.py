from time import sleep
from typing import List, Dict, Callable

from .device_mqtt import DeviceMqtt
from .device_serial import DeviceSerial
import logging


class DeviceElectricityCurrent(DeviceMqtt, DeviceSerial):
    def __init__(
            self,
            mqtt_publish: Callable[[DeviceMqtt, str, str], None],
            serial_send: Callable[[bytes], None],
    ):
        self.mqtt_publish = mqtt_publish
        self.serial_send = serial_send

    @property
    def device_id(self) -> str:
        return "electricity_current"

    @property
    def device_name(self) -> str:
        return "electricity_current"

    @property
    def device_tags(self) -> List[str]:
        return ["전기사용량"]

    @property
    def mqtt_device_type(self) -> str:
        return "text"

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
        if data.startswith(b'\xf7\x60\x01\x01\x03'):
            logging.info("aa")
            electricity_current = self.bytes_to_int(data[5:7])
            logging.info(str(electricity_current))
            self.mqtt_publish(self, "set", str(electricity_current))

    @property
    def additional_payload(self) -> Dict[str, str]:
        return {
            "command_topic": "~/set",
        }

    def receive_topic(self, topic: str, payload: str):
        return
        # if topic == "command":
        #     if payload == "heat":
        #         self.turn_on()
        #     elif payload == "off":
        #         self.turn_off()
        # elif topic == "set":
        #     while True:
        #         set_temperature: int = int(float(payload))
        #         self.serial_send(b'\x36' + (self.number + 16).to_bytes(1, "big") + b'\x44\x01' + (set_temperature & 0xFF).to_bytes(1, 'big'))
        #         if set_temperature == self.set_temperature :
        #             break
        #         logging.info("temp : {}, {}".format(str(set_temperature), str(self.set_temperature)))
        #         sleep(0.3)
