from abc import ABC, abstractmethod
from typing import Union

from app.domain import SurveyModel


class LoadSurveysRepo(ABC):
    @abstractmethod
    def load_all(self) -> Union[list[SurveyModel], None]:
        """Abstract method for loading all surveys from database"""
