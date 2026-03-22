from abc import ABC, abstractmethod
from typing import Tuple


class Storage(ABC):
    @abstractmethod
    def save(self, path: str, content: bytes) -> str:
        pass

    @abstractmethod
    def fetch(self, id: str) -> Tuple[bytes, str]:
        pass
