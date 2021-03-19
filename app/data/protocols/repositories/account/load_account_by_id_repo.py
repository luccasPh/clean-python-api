from abc import ABC, abstractmethod
from typing import Union

from app.domain import AccountModel


class LoadAccountByIdRepo(ABC):
    @abstractmethod
    def load_by_id(self, id: str, role: str = None) -> Union[AccountModel, None]:
        """Abstract method for load an account from db by id"""
