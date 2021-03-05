from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SurveyAnswer:
    image: str
    answer: str


@dataclass
class AddSurveyModel:
    question: str
    answers: list[SurveyAnswer]


class AddSurvey(ABC):
    @abstractmethod
    def add(self, data: AddSurveyModel):
        """Abstract method for creating an survey"""
