from enum import Enum, auto
from typing import List, Dict
from abc import *

from device import Device


class DeviceMqtt(Device, metaclass=ABCMeta):

    @property
    @abstractmethod
    def additional_payload(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def receive_topic(self, topic: str, payload: str):
        pass
