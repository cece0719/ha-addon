import http.server
import json
import datetime
import socketserver
from http import HTTPStatus
import logging
from theshopserial import TheShopSerial
from theshopmqtt import TheShopMQTT
from device_light import DeviceLight
from device_elevator import DeviceElevator

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

if __name__ == "__main__":
    logging.info("initialize serial...")
    mqtt = TheShopMQTT()
    serial = TheShopSerial()

    device_light_1 = DeviceLight(mqtt, serial, 1)
    DeviceLight(mqtt, serial, 2)
    DeviceLight(mqtt, serial, 3)
    DeviceElevator(mqtt, serial)

    mqtt.start()
    serial.start()


    class Handler(http.server.SimpleHTTPRequestHandler):
        def discover(self, body):
            body["header"]["name"] = "DiscoverAppliancesResponse"
            body["payload"] = {
                "discoveredAppliances": {
                    "applianceId": "light_1",
                    "applianceTypes": ["LIGHT"],
                    "actions": ["TurnOn", "TurnOff"],
                    "friendlyName": "거실 하나",
                    "tags": ["거실"]
                }
            }
            return json.dumps(body)

        def action(self, body):
            ret = {
                "header": body["header"],
                "payload": {}
            }
            header_name = body["header"]["name"]
            if header_name == "TurnOnRequest":
                ret["header"]["name"] = "TurnOnConfirmation"
                device_light_1.set_on()
            elif header_name == "TurnOffRequest":
                ret["header"]["name"] = "TurnOffConfirmation"
                device_light_1.set_off()

            return json.dumps(ret)

        def do_POST(self):
            logging.info(self.headers)
            logging.info(self.path)
            logging.info(self.request)
            logging.info(self.requestline)

            content_len = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_len)
            logging.info(body)
            logging.info(str(body))
            body_json = json.loads(body)
            logging.info(body_json)

            if body_json["header"]["name"] == "DiscoverAppliancesRequest":
                response = self.discover(body_json)
            else:
                response = self.action(body_json)

            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(response.encode("utf8"))


    logging.info("try http start")
    httpd = socketserver.TCPServer(('', 8001), Handler)
    httpd.serve_forever()
