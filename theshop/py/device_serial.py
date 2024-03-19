from enum import Enum, auto
from typing import List, Dict
from abc import *

from theshop.py.device import Device


class DeviceSerial(Device, metaclass=ABCMeta):

    @abstractmethod
    def receive_serial(self, data):
        pass
