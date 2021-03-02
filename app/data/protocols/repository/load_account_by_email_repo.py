from abc import ABC, abstractmethod

from app.domain import AccountModel


class LoadAccountByEmailRepo(ABC):
    @abstractmethod
    def load(self, email: str) -> AccountModel:
        """Abstract method for load an account from db by email"""
