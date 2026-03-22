from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save(self, path: str, content: bytes) -> str:
        pass
