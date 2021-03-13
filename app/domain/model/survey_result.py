from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SurveyResultAnswerModel:
    answer: str
    count: int
    percent: float
    image: Optional[str] = None


@dataclass
class SurveyResultModel:
    survey_id: str
    question: str
    answers: list[SurveyResultAnswerModel]
    date: datetime

    def __post_init__(self):
        list_answer = list(
            map(lambda data: SurveyResultAnswerModel(**data), self.answers)
        )
        self.answers = list_answer
