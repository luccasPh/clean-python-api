from dataclasses import asdict

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
            survey = asdict(self._load_survey_by_id_repo.load_by_id(survey_id))
            survey_result = SurveyResultModel(
                survey_id=survey.get("id"),
                question=survey.get("question"),
                answers=list(
                    map(
                        lambda item: dict(item, count=0, percent=0),
                        survey.get("answers"),
                    )
                ),
                date=survey.get("date"),
            )
        return survey_result
