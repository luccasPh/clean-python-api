from abc import ABC, abstractmethod
from typing import Union

from app.domain import SurveyModel


class LoadSurveyByIdRepo(ABC):
    @abstractmethod
    def load_by_id(self, id: str) -> Union[SurveyModel, None]:
        """Abstract method for loading a survey by id from database"""
