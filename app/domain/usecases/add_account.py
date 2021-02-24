from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..model.account import AccountModel


@dataclass
class AddAccountModel:
    name: str
    email: str
    password: str


class AddAccount(ABC):
    @abstractmethod
    def add(self, account_in: AddAccountModel) -> AccountModel:
        ...
