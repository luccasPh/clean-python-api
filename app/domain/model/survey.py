from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class SurveyAnswerModel:
    answer: str
    image: Optional[str] = None


@dataclass
class SurveyModel:
    id: str
    question: str
    answers: list[SurveyAnswerModel]
    date: datetime

    def __post_init__(self):
        list_answer = list(map(lambda data: SurveyAnswerModel(**data), self.answers))
        self.answers = list_answer
