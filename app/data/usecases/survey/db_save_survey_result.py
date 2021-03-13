from app.data import SaveSurveyResultRepo, LoadSurveyResultRepo
from app.domain import SaveSurveyResultModel, SurveyResultModel
from app.domain import SaveSurveyResult


class DbSaveSurveyResult(SaveSurveyResult):
    def __init__(
        self,
        save_survey_result_repo: SaveSurveyResultRepo,
        load_survey_result_repo: LoadSurveyResultRepo,
    ):
        self._save_survey_result_repo = save_survey_result_repo
        self._load_survey_result_repo = load_survey_result_repo

    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        self._save_survey_result_repo.save(data)
        survey_result = self._load_survey_result_repo.load_by_survey_id(data.survey_id)
        return survey_result
