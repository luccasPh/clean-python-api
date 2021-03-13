from abc import ABC, abstractmethod

from ...model.survey_result import SurveyResultModel


class LoadSurveyResult(ABC):
    @abstractmethod
    def save(self, survey_id: str) -> SurveyResultModel:
        """Abstract method for load a survey result"""
