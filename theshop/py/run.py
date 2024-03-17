import http.server
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

    DeviceLight(mqtt, serial, 1)
    DeviceLight(mqtt, serial, 2)
    DeviceLight(mqtt, serial, 3)
    DeviceElevator(mqtt, serial)

    mqtt.start()
    serial.start()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(b'Hello world')

    logging.info("try http start")
    httpd = socketserver.TCPServer(('', 8001), Handler)
    httpd.serve_forever()
