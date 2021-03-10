import pytest
from mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time

from app.data import DbSaveSurveyResult, SaveSurveyResultRepo
from app.domain import SurveyResultModel, SaveSurveyResultModel


class SaveSurveyResultRepoStub(SaveSurveyResultRepo):
    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        fake_survey_result = dict(
            id="any_id",
            account_id="any_account_id",
            survey_id="any_survey_id",
            answer="any_answer",
            date=datetime.utcnow(),
        )
        return SurveyResultModel(**fake_survey_result)


@pytest.fixture
def sut():
    save_survey_result_repo_stub = SaveSurveyResultRepoStub()
    yield DbSaveSurveyResult(save_survey_result_repo_stub)


@freeze_time("2021-03-09")
@patch.object(SaveSurveyResultRepoStub, "save")
def test_should_call_save_on_save_survey_result_repo_correct_values(
    mock_save: MagicMock, sut: DbSaveSurveyResult
):
    survey_result = SaveSurveyResultModel(
        survey_id="any_survey_id", account_id="any_account_id", answer="any_answer"
    )
    sut.save(survey_result)
    mock_save.assert_called_with(survey_result)
