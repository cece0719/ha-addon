import logging
from abc import *

from typing import Dict

from .device import Device
from .device_elevator import DeviceElevator
from .device_light import DeviceLight
from .device_light_total import DeviceLightTotal

class CallElevator(Device, metaclass=ABCMeta):
    @abstractmethod
    def call_elevator(self):
        pass

class DeviceClova(Device, metaclass=ABCMeta):
    def get_discovered_appliance(self):
        return {
            "applianceId" : self.device_id,
            "friendlyName" : self.device_name,
            "tags" : self.device_tags,
            "applianceTypes" : self.appliance_types,
            "actions" : self.clova_actions,
        }

    @property
    @abstractmethod
    def appliance_types(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def clova_actions(self) -> list[str]:
        pass

    @abstractmethod
    def action(self, body) -> Dict:
        pass