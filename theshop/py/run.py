import logging
import http.server
import json
import socketserver

from http import HTTPStatus
from theshopserial import TheShopSerial
from theshopmqtt import TheShopMQTT
from theshopclova import TheShopClova
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
    clova = TheShopClova()

    device_light_1 = DeviceLight(mqtt, serial, 1)
    DeviceLight(mqtt, serial, 2)
    DeviceLight(mqtt, serial, 3)
    DeviceElevator(mqtt, serial)

    mqtt.start()
    serial.start()


    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            content_len = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_len)
            body_json = json.loads(body)

            logging.info(body_json)

            header_name = body_json["header"]["name"]
            if header_name == "DiscoverAppliancesRequest":
                response = clova.discover(body_json)
            else:
                response = clova.action(body_json)

            logging.info(response)

            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(response.encode("utf8"))


    logging.info("try http start")
    httpd = socketserver.TCPServer(('', 8001), Handler)
    httpd.serve_forever()
