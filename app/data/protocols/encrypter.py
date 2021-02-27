from abc import ABC, abstractmethod


class Encrypter(ABC):
    @abstractmethod
    def encrypt(self, value: str) -> str:
        """Abstract method for encrypting a value"""
