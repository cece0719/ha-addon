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

    def add_device(self, device):
        appliance_id = device.clova["applianceId"]
        self.devices[appliance_id] = device
        discovered_appliance = copy.deepcopy(device.clova)
        discovered_appliance["actions"] = [*discovered_appliance["actions"].keys()]
        self.discoveredAppliances.append(discovered_appliance)

    def discover(self, body):
        body["header"]["name"] = "DiscoverAppliancesResponse"

        discoveredAppliances = []
        for device in self.devices:
            discovered_appliance = device.getDiscoveredAppliance()
            discoveredAppliances.append(discovered_appliance)

        ret = {
            "header": body["header"],
            "payload": {
                "discoveredAppliances": self.discoveredAppliances
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
