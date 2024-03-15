import logging


class DeviceLight:
    def __init__(self, mqtt, serial, number):
        self.number = number
        self.status = False
        self.mqtt = mqtt
        self.serial = serial
        mqtt.add_device(self)
        serial.add_device(self)

    def receive_mqtt(self, topic, payload):
        return

    def receive_serial(self, data):
        if data.startswith(b'\xf7\x0e\x1f\x81'):
            if data[4 + self.number] == 1:
                logging.info("light" + str(self.number) + "status on")
                self.status = True
            else:
                logging.info("light" + str(self.number) + "status off")
                self.status = False
