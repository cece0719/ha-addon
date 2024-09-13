import json
import logging
import sys
from typing import List

from device.device import Device
from device.device_elevator import DeviceElevator
from device.device_gas import DeviceGas
from device.device_light import DeviceLight
from device.device_light_total import DeviceLightTotal
from theshopclova import TheShopClova
from theshopmqtt import TheShopMQTT
from theshopserial import TheShopSerial

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

    devices: List[Device] = [
        DeviceLight(1, "거실1", ["거실"], mqtt.publish, serial.send),
        DeviceLight(2, "거실2", ["거실"], mqtt.publish, serial.send),
        DeviceLight(3, "복도", ["복도"], mqtt.publish, serial.send),
        DeviceLightTotal(mqtt.publish, serial.send),
        DeviceGas(mqtt.publish, serial.send),
        DeviceElevator(serial.send),
    ]

    mqtt.add_devices(devices)
    serial.add_devices(devices)
    clova.add_devices(devices)

    mqtt.start()
    serial.start()
    clova.start()
