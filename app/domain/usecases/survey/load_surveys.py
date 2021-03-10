from abc import ABC, abstractmethod
from typing import Union

from ...model.survey import SurveyModel


class LoadSurveys(ABC):
    @abstractmethod
    def load(self) -> Union[list[SurveyModel], None]:
        """Abstract method for load all surveys"""
