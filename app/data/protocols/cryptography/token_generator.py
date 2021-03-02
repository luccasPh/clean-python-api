from abc import ABC, abstractmethod


class TokenGenerator(ABC):
    @abstractmethod
    def generate(self, id: str) -> str:
        """Abstract method for generate user access token"""
