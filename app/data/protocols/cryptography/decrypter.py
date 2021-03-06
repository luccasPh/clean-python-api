from abc import ABC, abstractmethod


class Decrypter(ABC):
    @abstractmethod
    def decrypt(self, value: str) -> str:
        """Abstract method for decrypt access token"""
