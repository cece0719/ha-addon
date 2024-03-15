import logging


class DeviceLight:
    def __init__(self, number):
        self.number = number
        self.status = False

    def receive_mqtt(self, topic, payload):
        ""

    def receive_serial(self, data):
        if data.startswith(b'\xf7\x0e\x1f\x81'):
            if data[4 + self.number] == 1:
                logging.info("light" + str(self.number) + "status on")
                self.status = True
            else:
                logging.info("light" + str(self.number) + "status on")
                self.status = False
