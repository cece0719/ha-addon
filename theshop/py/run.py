import json
import logging
import http.server
import socketserver
import sys
from http import HTTPStatus

from typing import List, Callable
from device.device import Device
from device.device_light import DeviceLight
from device.device_light_total import DeviceLightTotal
from device.device_elevator import DeviceElevator
from device.device_gas import DeviceGas
from device.device_mqtt import DeviceMqtt
from option import Option
from theshopclova import TheShopClova
from theshopserial import TheShopSerial
from theshopmqtt import TheShopMQTT

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

if __name__ == "__main__":
    logging.info("initialize serial...")
    option = Option(sys.argv[1])
    logging.info(option.get("type"))
    mqtt = TheShopMQTT(option)
    serial = TheShopSerial(option)
    clova = TheShopClova(option)

    mqtt_publish: Callable[[DeviceMqtt, str, str], None] = mqtt.publish
    serial_send: Callable[[bytes], None] = \
        lambda command: serial.send(command)

    devices: List[Device] = [
        DeviceLight(1, "거실1", ["거실"], mqtt_publish, serial_send),
        DeviceLight(2, "거실2", ["거실"], mqtt_publish, serial_send),
        DeviceLight(3, "복도", ["복도"], mqtt_publish, serial_send),
        DeviceLightTotal(mqtt_publish, serial_send),
        DeviceGas(mqtt_publish, serial_send),
        DeviceElevator(serial_send),
    ]

    mqtt.add_devices(devices)
    serial.add_devices(devices)
    # clova.add_devices(devices)

    # DeviceLight(1, "거실1", ["거실"], mqtt, serial, clova)
    # DeviceLight(2, "거실2", ["거실"], mqtt, serial, clova)
    # DeviceLight(3, "복도", ["복도"], mqtt, serial, clova)
    # DeviceElevator(mqtt, serial, clova)

    mqtt.start()
    serial.start()


    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(b'Hello world')
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
