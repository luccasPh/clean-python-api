from abc import ABC, abstractmethod

from app.domain import AddAccountModel, AccountModel


class AddAccountRepo(ABC):
    @abstractmethod
    def add(self, data: AddAccountModel) -> AccountModel:
        """Abstract method for saving data to the database"""
