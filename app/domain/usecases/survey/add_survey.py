from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...model.survey import SurveyAnswerModel


@dataclass
class AddSurveyModel:
    question: str
    answers: list[SurveyAnswerModel]

    def __post_init__(self):
        list_answer = list(map(lambda data: SurveyAnswerModel(**data), self.answers))
        self.answers = list_answer


class AddSurvey(ABC):
    @abstractmethod
    def add(self, data: AddSurveyModel):
        """Abstract method for creating an survey"""
