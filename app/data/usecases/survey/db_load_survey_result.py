from app.domain import LoadSurveyResult, SurveyResultModel
from app.data import LoadSurveyResultRepo, LoadSurveyByIdRepo


class DbLoadSurveyResult(LoadSurveyResult):
    def __init__(
        self,
        load_survey_result_repo: LoadSurveyResultRepo,
        load_survey_by_id_repo: LoadSurveyByIdRepo,
    ):
        self._load_survey_result_repo = load_survey_result_repo
        self._load_survey_by_id_repo = load_survey_by_id_repo

    def load(self, survey_id: str) -> SurveyResultModel:
        survey_result = self._load_survey_result_repo.load_by_survey_id(survey_id)
        if not survey_result:
            return self._load_survey_by_id_repo.load_by_id(survey_id)
        return survey_result
