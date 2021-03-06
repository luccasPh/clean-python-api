from abc import ABC, abstractmethod
from typing import Union

from app.domain import AccountModel


class LoadAccountByEmailRepo(ABC):
    @abstractmethod
    def load_by_email(self, email: str) -> Union[AccountModel, None]:
        """Abstract method for load an account from db by email"""
