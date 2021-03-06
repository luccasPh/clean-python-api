from abc import ABC, abstractmethod

from app.domain import AddSurveyModel


class AddSurveyRepo(ABC):
    @abstractmethod
    def add(self, data: AddSurveyModel):
        """Abstract method for saving data to the database"""
