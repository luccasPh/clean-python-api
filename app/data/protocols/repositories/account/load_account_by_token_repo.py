from abc import ABC, abstractmethod
from typing import Union

from app.domain import AccountModel


class LoadAccountByTokenRepo(ABC):
    @abstractmethod
    def load_by_token(
        self, access_token: str, role: str = None
    ) -> Union[AccountModel, None]:
        """Abstract method for load an account from db by access token"""
