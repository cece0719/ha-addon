import json
import logging
import sys
from typing import List

from device.device import Device
from device.device_elevator import DeviceElevator
from device.device_gas import DeviceGas
from device.device_light import DeviceLight
from device.device_boiler import DeviceBoiler
from device.device_light_total import DeviceLightTotal
from theshopclova import TheShopClova
from theshopmqtt import TheShopMQTT
from theshopserial import TheShopSerial

if __name__ == "__main__":
    option = json.load(open(sys.argv[1]))

    if option["logLevel"] == "DEBUG":
        log_level=logging.DEBUG
    elif option["logLevel"] == "INFO":
        log_level=logging.INFO
    else:
        log_level=logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logging.info("initialize serial...")

    mqtt = TheShopMQTT(option)
    serial = TheShopSerial(option)
    clova = TheShopClova(option)

    devices: List[Device] = [
        DeviceLight(1, 1, "거실1", ["거실"], mqtt.publish, serial.send),
        DeviceLight(1, 2, "거실2", ["거실"], mqtt.publish, serial.send),
        DeviceLight(1, 3, "복도", ["복도"], mqtt.publish, serial.send),
        DeviceLight(2, 1, "안방", ["안방"], mqtt.publish, serial.send),
        DeviceLight(3, 1, "하온이방", ["하온이방","애들방"], mqtt.publish, serial.send),
        DeviceLight(4, 1, "하빈이방", ["하빈이방", "애들방"], mqtt.publish, serial.send),
        DeviceLight(5, 1, "알파룸", ["알파룸", "서재"], mqtt.publish, serial.send),
        DeviceBoiler(1, "거실", ["거실"], mqtt.publish, serial.send),
        DeviceBoiler(2, "안방", ["안방"], mqtt.publish, serial.send),
        DeviceBoiler(3, "하온이방", ["하온이방"], mqtt.publish, serial.send),
        DeviceBoiler(4, "하빈이방", ["하빈이방"], mqtt.publish, serial.send),
        DeviceBoiler(5, "알파룸", ["알파룸"], mqtt.publish, serial.send),
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
