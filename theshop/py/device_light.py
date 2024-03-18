import logging


class DeviceLight:
    def __init__(self, number, name, tags, mqtt, serial, clova):
        self.number = number
        self.status = False
        self.mqtt = mqtt
        self.serial = serial
        self.publishes = [
            {
                "topic": "homeassistant/light/cece0719/light_{}/config".format(self.number),
                "payload": {
                    "unique_id": "light_{}".format(self.number),
                    "command_topic": "cece0719/light_{}/command".format(self.number),
                    "state_topic": "cece0719/light_{}/state".format(self.number),
                    "payload_on": 'ON',
                    "payload_off": 'OFF',
                }
            }
        ]
        self.clova = {
            "applianceId": "light_{}".format(self.number),
            "applianceTypes": ["LIGHT"],
            "friendlyName": name,
            "tags": tags,
            "actions": {
                "TurnOn": lambda: self.set_on(),
                "TurnOff": lambda: self.set_off(),
            },
        }

        mqtt.add_device(self)
        serial.add_device(self)
        clova.add_device(self)

    def receive_mqtt(self, topic, payload):
        if topic == "cece0719/light_{}/command".format(self.number):
            logging.info("light" + str(self.number) + "command " + str(payload))
            if payload == "ON":
                self.set_on()
            elif payload == "OFF":
                self.set_off()
        return

    def receive_serial(self, data):
        if data.startswith(b'\xf7\x0e\x1f\x81'):
            if data[5 + self.number] == 1:
                logging.info("light" + str(self.number) + "status on")
                self.mqtt.publish("cece0719/light_{}/state".format(self.number), "ON")
                self.status = True
            else:
                logging.info("light" + str(self.number) + "status off")
                self.mqtt.publish("cece0719/light_{}/state".format(self.number), "OFF")
                self.status = False

    def set_on(self):
        self.serial.send(b'\x0E' + (self.number + 16).to_bytes(1, "big") + b'\x41\x01\x01')

    def set_off(self):
        self.serial.send(b'\x0E' + (self.number + 16).to_bytes(1, "big") + b'\x41\x01\x00')
