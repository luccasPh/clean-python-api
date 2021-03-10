from app.data import SaveSurveyResultRepo
from app.domain import SaveSurveyResultModel, SurveyResultModel
from app.domain import SaveSurveyResult


class DbSaveSurveyResult(SaveSurveyResult):
    def __init__(self, save_survey_result_repo: SaveSurveyResultRepo):
        self._save_survey_result_repo = save_survey_result_repo

    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        survey_result = self._save_survey_result_repo.save(data)
        return survey_result
