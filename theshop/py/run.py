import logging
from theshopserial import TheShopSerial
from theshopmqtt import TheShopMQTT
from device_light import DeviceLight


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)


if __name__ == "__main__":
    logging.info("initialize serial...")
    mqtt = TheShopMQTT()
    serial = TheShopSerial()

    device_light1=DeviceLight(1)
    device_light2=DeviceLight(2)
    device_light3=DeviceLight(3)
    device_light4=DeviceLight(4)

    mqtt.add_device(device_light1)
    mqtt.add_device(device_light2)
    mqtt.add_device(device_light3)
    mqtt.add_device(device_light4)
    serial.add_device(device_light1)
    serial.add_device(device_light2)
    serial.add_device(device_light3)
    serial.add_device(device_light4)

    mqtt.start()
    serial.start()
