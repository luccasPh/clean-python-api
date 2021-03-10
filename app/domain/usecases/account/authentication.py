from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AuthenticationModel:
    email: str
    password: str


class Authentication(ABC):
    @abstractmethod
    def auth(self, authentication: AuthenticationModel) -> str:
        """Abstract method for authentication user"""
