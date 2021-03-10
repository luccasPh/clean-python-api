from typing import Union

from app.data import LoadSurveyByIdRepo
from app.domain import LoadSurveyById, SurveyModel


class DbLoadSurveyById(LoadSurveyById):
    def __init__(self, load_survey_by_id_repo: LoadSurveyByIdRepo):
        self._load_survey_by_id_repo = load_survey_by_id_repo

    def load_by_id(self, id: str) -> Union[SurveyModel, None]:
        self._load_survey_by_id_repo.load_by_id(id)
