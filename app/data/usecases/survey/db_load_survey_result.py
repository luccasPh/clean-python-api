from app.domain import LoadSurveyResult, SurveyResultModel
from app.data import LoadSurveyResultRepo


class DbLoadSurveyResult(LoadSurveyResult):
    def __init__(self, load_survey_result_repo: LoadSurveyResultRepo):
        self._load_survey_result_repo = load_survey_result_repo

    def load(self, survey_id: str) -> SurveyResultModel:
        survey_result = self._load_survey_result_repo.load_by_survey_id(survey_id)
        return survey_result
