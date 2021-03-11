from abc import ABC, abstractmethod
from typing import Union

from ...model.survey import SurveyModel


class LoadSurveyById(ABC):
    @abstractmethod
    def load_by_id(self, id: str) -> Union[SurveyModel, None]:
        """Abstract method for load a survey by id"""
