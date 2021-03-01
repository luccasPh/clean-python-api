from abc import ABC, abstractmethod


class Authentication(ABC):
    @abstractmethod
    def auth(self, valid_data: dict) -> str:
        """Abstract method for authentication user"""
