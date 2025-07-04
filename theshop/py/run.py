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
from device.device_lock import DeviceLock
from device.device_electricity_current import DeviceElectricityCurrent
from device.device_electricity_all import DeviceElectricityAll
from device.device_electricity_room import DeviceElectricityRoom

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

    deviceLightTotal = DeviceLightTotal(mqtt.publish, serial.send)

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
        DeviceGas(mqtt.publish, serial.send),
        deviceLightTotal,
        DeviceElevator(deviceLightTotal, serial.send),
        DeviceLock(mqtt.publish, serial.send),
        DeviceElectricityCurrent(mqtt.publish, serial.send),
        DeviceElectricityAll(mqtt.publish, serial.send),
        # 방별 전력량 센서들
        DeviceElectricityRoom(1, "1번", ["1번"], mqtt.publish, serial.send),
        DeviceElectricityRoom(2, "2번", ["2번"], mqtt.publish, serial.send),
        DeviceElectricityRoom(3, "3번", ["3번"], mqtt.publish, serial.send),
        DeviceElectricityRoom(4, "4번", ["4번"], mqtt.publish, serial.send),
        DeviceElectricityRoom(5, "5번", ["5번"], mqtt.publish, serial.send),
        DeviceElectricityRoom(9, "6번", ["6번"], mqtt.publish, serial.send),
    ]

    mqtt.add_devices(devices)
    serial.add_devices(devices)

    mqtt.start()
    serial.start()
    
    # 메인 스레드가 종료되지 않도록 대기
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("애드온 종료 중...")
