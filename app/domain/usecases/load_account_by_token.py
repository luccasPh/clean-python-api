from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..model.account import AccountModel


@dataclass
class AddAccountModel:
    name: str
    email: str
    password: str


class LoadAccountByToken(ABC):
    @abstractmethod
    def load(self, access_token: str, role: str = None) -> AccountModel:
        """Abstract method for load an account by token field"""
