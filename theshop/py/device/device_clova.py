from abc import *

from .device import Device


class DeviceClova(Device, metaclass=ABCMeta):

    @abstractmethod
    def getDiscoveredAppliance(self):
        pass
