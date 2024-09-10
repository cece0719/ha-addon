import json
import logging
import http.server
import socketserver
import sys
from http import HTTPStatus

from typing import List, Callable
from device.device import Device
from device.device_light import DeviceLight
from device.device_light_total import DeviceLightTotal
from device.device_elevator import DeviceElevator
from device.device_gas import DeviceGas
from device.device_mqtt import DeviceMqtt
from theshopclova import TheShopClova
from theshopserial import TheShopSerial
from theshopmqtt import TheShopMQTT

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

if __name__ == "__main__":
    logging.info("initialize serial...")
    option = json.load(open(sys.argv[1]))
    mqtt = TheShopMQTT(option)
    serial = TheShopSerial(option)
    clova = TheShopClova(option)

    mqtt_publish: Callable[[DeviceMqtt, str, str], None] = mqtt.publish
    serial_send: Callable[[bytes], None] = \
        lambda command: serial.send(command)

    devices: List[Device] = [
        DeviceLight(1, "거실1", ["거실"], mqtt_publish, serial_send),
        DeviceLight(2, "거실2", ["거실"], mqtt_publish, serial_send),
        DeviceLight(3, "복도", ["복도"], mqtt_publish, serial_send),
        DeviceLightTotal(mqtt_publish, serial_send),
        DeviceGas(mqtt_publish, serial_send),
        DeviceElevator(serial_send),
    ]

    mqtt.add_devices(devices)
    serial.add_devices(devices)
    clova.add_devices(devices)

    mqtt.start()
    serial.start()
    clova.start()