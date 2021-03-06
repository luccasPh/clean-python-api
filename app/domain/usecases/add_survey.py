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

    def __post_init__(self):
        list_answer = list(map(lambda data: SurveyAnswer(**data), self.answers))
        self.answers = list_answer


class AddSurvey(ABC):
    @abstractmethod
    def add(self, data: AddSurveyModel):
        """Abstract method for creating an survey"""
