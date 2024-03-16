import logging


class DeviceElevator:
    def __init__(self, mqtt, serial):
        self.mqtt = mqtt
        self.serial = serial
        mqtt.add_device(self)
        self.publishes = [
            {
                "topic": "homeassistant/button/cece0719/button_elevator/config",
                "payload": {
                    "unique_id": "button_elevator",
                    "command_topic": "cece0719/button_elevator/command",
                    # "state_topic": "cece0719/button_elevator/state",
                    # "payload_on": 'ON',
                    # "payload_off": 'OFF',
                }
            }
        ]

    def receive_mqtt(self, topic, payload):
        if topic == "cece0719/button_elevator/command" and payload == "PRESS":
            self.serial.send(b'\x33\x01\x81\x03\x00\x20\x00')
