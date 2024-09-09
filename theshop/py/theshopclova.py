import copy
import http.server
import json
import datetime

from http import HTTPStatus

# import paho.mqtt.client as paho_mqtt
import json
import socketserver
import logging

from option import Option


class TheShopClova:
    def __init__(
            self,
            option: Option
    ):
        self.devices = {}
        self.discoveredAppliances = []

    def add_device(self, device):
        appliance_id = device.clova["applianceId"]
        self.devices[appliance_id] = device
        discovered_appliance = copy.deepcopy(device.clova)
        discovered_appliance["actions"] = [*discovered_appliance["actions"].keys()]
        self.discoveredAppliances.append(discovered_appliance)

    def discover(self, body):
        body["header"]["name"] = "DiscoverAppliancesResponse"
        ret = {
            "header": body["header"],
            "payload": {"discoveredAppliances": self.discoveredAppliances}
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
