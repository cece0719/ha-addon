import copy
import http.server
import json
import datetime

from http import HTTPStatus

# import paho.mqtt.client as paho_mqtt
import json
import socketserver
import logging


class Option:
    def __init__(
            self,
            optionFile: str,
    ):
        self.optionFile = optionFile

    def get(self, key):
        option = open(self.optionFile)
        return json.load(option)[key]
