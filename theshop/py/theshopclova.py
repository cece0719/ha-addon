import http.server
# import paho.mqtt.client as paho_mqtt
import json
import logging
import socketserver
from http import HTTPStatus
from typing import List, Dict

from device.device import Device
from device.device_clova import DeviceClova


class TheShopClova:
    def __init__(self, option):
        self.option = option
        self.devices: Dict[str, DeviceClova] = {}
        self.discoveredAppliances = []

    def discover(self, body):
        body["header"]["name"] = "DiscoverAppliancesResponse"

        discovered_appliances = []
        for device in self.devices.values():
            discovered_appliance = device.get_discovered_appliance()
            discovered_appliances.append(discovered_appliance)

        return json.dumps({
            "header": body["header"],
            "payload": {
                "discoveredAppliances": discovered_appliances
            }
        })

    def action(self, body):
        payload = body["payload"]
        appliance = payload["appliance"]
        appliance_id = appliance["applianceId"]

        ret = self.devices[appliance_id].action(body)
        return json.dumps(ret)

    def add_devices(self, devices: List[Device]):
        for device in devices:
            if isinstance(device, DeviceClova):
                self.devices[device.device_id] = device

    def start(self):
        clova = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_POST(self):
                content_len = int(self.headers.get("Content-Length"))
                body = self.rfile.read(content_len)
                body_json: Dict = json.loads(body)
                logging.info("http request : {}".format(json.dumps(body_json)))

                header_name = body_json["header"]["name"]
                if header_name == "DiscoverAppliancesRequest":
                    response = clova.discover(body_json)
                else:
                    response = clova.action(body_json)

                logging.info("http response : {}".format(response))

                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(response.encode("utf8"))

        logging.info("try http start")
        httpd = socketserver.TCPServer(('', 8001), Handler)
        httpd.serve_forever()
