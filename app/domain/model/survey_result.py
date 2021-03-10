from dataclasses import dataclass
from datetime import datetime


@dataclass
class SurveyResultModel:
    id: str
    survey_id: str
    account_id: str
    answer: str
    date: datetime
