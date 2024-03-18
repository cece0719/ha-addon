import http.server
import json
import datetime

from http import HTTPStatus

import paho.mqtt.client as paho_mqtt
import json
import socketserver
import logging


class TheShopClova:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def discover(self, body):
        discoveredAppliances = []
        for device in self.devices:
            clova = device.clova
            discoveredAppliances.append({
                "applianceId": clova["applianceId"],
                "applianceTypes": clova["applianceTypes"],
                "actions": clova["actions"].keys(),
                "friendlyName": clova["friendlyName"],
            })

        body["header"]["name"] = "DiscoverAppliancesResponse"
        ret = {
            "header": body["header"],
            "payload": {"discoveredAppliances": discoveredAppliances}
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

        command = header_name.replace("Request", "")
        ret["header"]["name"] = (command
                                 .replace("TurnOn", "TurnOnConfirmation")
                                 .replace("TurnOff", "TurnOffConfirmation")
                                 )

        for device in self.devices:
            if device.clova["applianceId"] == appliance_id:
                device.clova["actions"][command]()

        return json.dumps(ret)
