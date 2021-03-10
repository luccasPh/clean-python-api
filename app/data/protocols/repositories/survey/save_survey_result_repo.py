from abc import ABC, abstractmethod

from app.domain import SaveSurveyResultModel, SurveyResultModel


class SaveSurveyResultRepo(ABC):
    @abstractmethod
    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        """Abstract method to save a survey result data"""
