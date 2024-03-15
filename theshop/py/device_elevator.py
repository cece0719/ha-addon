import logging


class DeviceElevator:
    def __init__(self, mqtt, serial):
        self.mqtt = mqtt
        self.serial = serial
        mqtt.add_device(self)
        # serial.add_device(self)

    def receive_mqtt(self, topic, payload):
        if topic == "cece0719/elevator":
            logging.info("getElevatorCall")
            # self.serial.send(b'\xf7\x33\x01\x81\x03\x00\x20\x00')
