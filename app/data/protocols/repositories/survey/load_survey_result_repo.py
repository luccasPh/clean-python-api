from abc import ABC, abstractmethod
from typing import Union

from app.domain import SurveyResultModel


class LoadSurveyResultRepo(ABC):
    @abstractmethod
    def load_by_survey_id(self, survey_id) -> Union[SurveyResultModel, None]:
        """Abstract method to load a survey result by survey id on database"""
