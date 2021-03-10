from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...model.survey_result import SurveyResultModel


@dataclass
class SaveSurveyResultModel:
    survey_id: str
    account_id: str
    answer: str


class SaveSurveyResult(ABC):
    @abstractmethod
    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        """Abstract method for save an survey result"""
