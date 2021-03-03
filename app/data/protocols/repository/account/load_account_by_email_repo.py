from abc import ABC, abstractmethod

from app.domain import AccountModel


class LoadAccountByEmailRepo(ABC):
    @abstractmethod
    def load_by_email(self, email: str) -> AccountModel:
        """Abstract method for load an account from db by email"""
