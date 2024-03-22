from abc import *

from .device import Device


class DeviceSerial(Device, metaclass=ABCMeta):

    @abstractmethod
    def receive_serial(self, data):
        pass
