import logging


class DeviceLight:
    def __init__(self, mqtt, serial, number):
        self.number = number
        self.status = False
        self.mqtt = mqtt
        self.serial = serial
        self.publishes = [
            {
                "topic": "homeassistant/switch/cece0719/switch_{}/config".format(self.number),
                "payload": {
                    "unique_id": "switch_{}".format(self.number),
                    "command_topic": "cece0719/switch_{}/command".format(self.number),
                    "payload_on": 'ON',
                    "payload_off": 'OFF',
                }
            }
        ]

        mqtt.add_device(self)
        serial.add_device(self)

    def receive_mqtt(self, topic, payload):
        if topic == "cece0719/switch_{}/command".format(self.number):
            logging.info("light" + str(self.number) + "command " + str(payload))

            data = b'\x0E'
            data += (self.number+16).to_bytes(1, "big")
            data += b'\x41\x01'
            if payload == "ON":
                data += b'\x01'
            else:
                data += b'\x00'

            self.serial.send(data)
        return

    def receive_serial(self, data):
        if data.startswith(b'\xf7\x0e\x1f\x81'):
            if data[4 + self.number] == 1:
                logging.info("light" + str(self.number) + "status on")
                self.status = True
            else:
                logging.info("light" + str(self.number) + "status off")
                self.status = False
