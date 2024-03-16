import logging
from theshopserial import TheShopSerial
from theshopmqtt import TheShopMQTT
from device_light import DeviceLight
from device_elevator import DeviceElevator

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)

if __name__ == "__main__":
    logging.info("initialize serial...")
    mqtt = TheShopMQTT()
    serial = TheShopSerial()

    DeviceLight(mqtt, serial, 1)
    DeviceLight(mqtt, serial, 2)
    DeviceLight(mqtt, serial, 3)
    DeviceElevator(mqtt, serial)

    mqtt.start()
    serial.start()
