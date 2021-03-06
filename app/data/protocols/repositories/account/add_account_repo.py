from abc import ABC, abstractmethod

from app.domain import AddAccountModel


class AddAccountRepo(ABC):
    @abstractmethod
    def add(self, data: AddAccountModel):
        """Abstract method for saving data to the database"""
