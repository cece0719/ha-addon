from typing import List, Dict
from abc import *


class Device(metaclass=ABCMeta):
    @property
    @abstractmethod
    def device_id(self) -> str:
        pass

    @property
    @abstractmethod
    def device_name(self) -> str:
        pass

    @property
    @abstractmethod
    def device_tags(self) -> List[str]:
        pass