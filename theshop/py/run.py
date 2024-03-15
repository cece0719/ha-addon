import logging
from theshopserial import TheShopSerial
from theshopmqtt import TheShopMQTT


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S"
)


if __name__ == "__main__":
    logging.info("initialize serial...")
    mqtt = TheShopMQTT()
    serial = TheShopSerial()

    mqtt.start()
    serial.start()
