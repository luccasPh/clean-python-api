from typing import Union

from app.data import LoadSurveysRepo
from app.domain import LoadSurveys, SurveyModel


class DbLoadSurveys(LoadSurveys):
    def __init__(self, load_surveys_repo: LoadSurveysRepo):
        self._load_surveys_repo = load_surveys_repo

    def load(self) -> Union[list[SurveyModel], None]:
        surveys = self._load_surveys_repo.load_all()
        return surveys
