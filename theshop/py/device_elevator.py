import logging


class DeviceElevator:
    def __init__(self, mqtt, serial, clova):
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
        self.clova = {
            "applianceId": "elevator",
            "applianceTypes": ["BUILDING_ELEVATOR_CALLER"],
            "actions": {
                "CallElevator": lambda: self.call_elevator()
            },
        }

    def receive_mqtt(self, topic, payload):
        if topic == "cece0719/button_elevator/command" and payload == "PRESS":
            self.call_elevator()

    def call_elevator(self):
        self.serial.send(b'\x33\x01\x81\x03\x00\x20\x00')
