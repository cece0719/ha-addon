import copy
import http.server
import json
import datetime

from http import HTTPStatus

# import paho.mqtt.client as paho_mqtt
import json
import socketserver
import logging

from typing import List, Dict

from device.device_clova import DeviceClova
from device.device import Device


class TheShopClova:
    def __init__(
            self,
            option
    ):
        self.option = option
        self.devices: Dict[str, DeviceClova] = {}
        self.discoveredAppliances = []

    def discover(self, body):
        body["header"]["name"] = "DiscoverAppliancesResponse"

        discovered_appliances = []
        for device in self.devices.values():
            discovered_appliance = device.getDiscoveredAppliance()
            discovered_appliances.append(discovered_appliance)

        ret = {
            "header": body["header"],
            "payload": {
                "discoveredAppliances": discovered_appliances
            }
        }
        return json.dumps(ret)

    def action(self, body):
        ret = {
            "header": body["header"],
            "payload": {}
        }
        header = body["header"]
        payload = body["payload"]

        appliance = payload["appliance"]
        appliance_id = appliance["applianceId"]
        header_name = header["name"]

        action = self.devices[appliance_id]["actions"][header_name]
        response_header = action()
        ret["header"]["name"] = response_header

        return json.dumps(ret)

    def add_devices(self, devices: List[Device]):
        for device in devices:
            if isinstance(device, DeviceClova):
                self.devices[device.device_id] = device
