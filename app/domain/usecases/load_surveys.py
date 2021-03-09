from abc import ABC, abstractmethod

from ..model.survey import SurveyModel


class LoadSurveys(ABC):
    @abstractmethod
    def load(self) -> list[SurveyModel]:
        """Abstract method for load all surveys"""
