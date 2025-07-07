from typing import List, Dict

import paho.mqtt.client as paho_mqtt
import json
import time
import logging

from device.device import Device
from device.device_mqtt import DeviceMqtt


class TheShopMQTT:
    def __init__(self, option):
        self.option = option
        self.devices: Dict[str, DeviceMqtt] = {}

        self.mqtt_prefix = "cece0719"
        self.is_connect = False
        self.mqtt = paho_mqtt.Client()

    def add_devices(self, devices: List[Device]):
        for device in devices:
            if isinstance(device, DeviceMqtt):
                self.devices[device.device_id] = device

    def on_connect(self, mqtt, userdata, flags, rc):
        self.is_connect = True
        self.mqtt.subscribe("{}/#".format(self.mqtt_prefix), 0)
        for device in self.devices.values():
            topic = "homeassistant/{}/{}/{}/config".format(device.mqtt_device_type, self.mqtt_prefix, device.device_id)
            payload = {
                "unique_id": device.device_id,
                "name": device.device_name,
                "~": "{}/{}".format(self.mqtt_prefix, device.device_id),
            }
            payload.update(device.additional_payload)
            payload["device"] = {
                "ids": ["cece0719 the shop"],
                "name": "cece0719 the shop",
                "mf": "cece0719 mf",
                "mdl": "cece0719 the shop mdl",
                "sw": "cece0719/ha_addons/the_shop",
            }
            self.mqtt.publish(topic, json.dumps(payload))
        logging.info("mqtt on connect success")

    def on_disconnect(self, mqtt, userdata, rc):
        logging.warning(f"MQTT 연결이 끊어졌습니다! (코드: {rc})")
        self.is_connect = False
        
        # 자동 재연결 시도
        if rc != 0:
            logging.info("MQTT 자동 재연결을 시도합니다...")
            try:
                self.mqtt.reconnect()
                logging.info("MQTT 재연결 성공!")
            except Exception as e:
                logging.error(f"MQTT 재연결 실패: {e}")
                # 재연결 실패시 5초 후 다시 시도
                time.sleep(5)
                try:
                    self.mqtt.reconnect()
                    logging.info("MQTT 재연결 재시도 성공!")
                except Exception as e2:
                    logging.error(f"MQTT 재연결 재시도 실패: {e2}")

    def on_message(self, mqtt, userdata, msg):
        logging.debug("get messaged {}".format(msg.topic))
        logging.debug("get payload {}".format(msg.payload.decode()))
        topic: str = msg.topic
        topics = topic.split("/")
        device_id = topics[1]
        device = self.devices[device_id]
        payload = msg.payload.decode()

        device.receive_topic("/".join(topics[2:]), payload)

    def publish(self, device: DeviceMqtt, topic: str, payload: str) -> None:
        self.mqtt.publish("{}/{}/{}".format(self.mqtt_prefix, device.device_id, topic), payload)

    def start(self):
        self.mqtt.on_connect = (lambda mqtt, userdata, flags, rc: self.on_connect(mqtt, userdata, flags, rc))
        self.mqtt.on_disconnect = (lambda mqtt, userdata, rc: self.on_disconnect(mqtt, userdata, rc))
        self.mqtt.on_message = (lambda mqtt, userdata, msg: self.on_message(mqtt, userdata, msg))
        self.mqtt.username_pw_set("xxx", "xxx")
        
        # MQTT 연결 무한 재시도
        attempt = 0
        while True:
            try:
                self.mqtt.connect("192.168.68.63")
                logging.info(f"MQTT 연결 성공! (시도 횟수: {attempt + 1})")
                break
            except Exception as e:
                attempt += 1
                logging.warning(f"MQTT 연결 실패 (시도 횟수: {attempt}) - {e}")
                logging.info("5초 후 재시도...")
                time.sleep(5)
        
        self.mqtt.loop_start()

        while not self.is_connect:
            logging.info("waiting MQTT connected")
            time.sleep(1)

        logging.info("MQTT connect success!!")
