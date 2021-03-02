from abc import ABC, abstractmethod


class HashComparer(ABC):
    @abstractmethod
    def compare(self, value: str, hash: str) -> bool:
        """Abstract method for compare a value with a hash"""
