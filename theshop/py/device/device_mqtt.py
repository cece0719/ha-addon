from typing import Dict, Callable
from abc import *

from device.device import Device


class DeviceMqtt(Device, metaclass=ABCMeta):

    @property
    @abstractmethod
    def additional_payload(self) -> Dict[str, str]:
        pass

    @property
    @abstractmethod
    def mqtt_device_type(self) -> str:
        pass

    @abstractmethod
    def receive_topic(self, topic: str, payload: str):
        pass
