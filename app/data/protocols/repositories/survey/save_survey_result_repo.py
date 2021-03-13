from abc import ABC, abstractmethod

from app.domain import SaveSurveyResultModel


class SaveSurveyResultRepo(ABC):
    @abstractmethod
    def save(self, data: SaveSurveyResultModel):
        """Abstract method to save a survey result data"""
