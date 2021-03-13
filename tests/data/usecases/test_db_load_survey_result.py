import pytest
from mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time

from app.data import DbLoadSurveyResult, LoadSurveyResultRepo
from app.domain import SurveyResultModel


class LoadSurveyResultRepoStub(LoadSurveyResultRepo):
    def load_by_survey_id(self, survey_id: str) -> SurveyResultModel:
        fake_survey_result = dict(
            survey_id="any_survey_id",
            question="any_question",
            answers=[
                dict(answer="any_answer", count=1, percent=40, image="any_image"),
                dict(answer="other_answer", count=2, percent=60, image="any_image"),
            ],
            date=datetime.utcnow(),
        )
        return SurveyResultModel(**fake_survey_result)


@pytest.fixture
def sut():
    load_survey_result_repo_stub = LoadSurveyResultRepoStub()
    yield DbLoadSurveyResult(load_survey_result_repo_stub)


@freeze_time("2021-03-09")
@patch.object(LoadSurveyResultRepoStub, "load_by_survey_id")
def test_should_call_load_by_survey_id_on_load_survey_result_repo_correct_values(
    load_by_survey_id: MagicMock, sut: DbLoadSurveyResult
):
    sut.load("any_survey_id")
    load_by_survey_id.assert_called_with("any_survey_id")


@patch.object(LoadSurveyResultRepoStub, "load_by_survey_id")
def test_should_raise_exception_if_load_survey_result_repo_raise(
    load_by_survey_id: MagicMock, sut: DbLoadSurveyResult
):
    load_by_survey_id.side_effect = Exception("Error on matrix")
    with pytest.raises(Exception) as excinfo:
        assert sut.load("any_survey_id")
    assert type(excinfo.value) is Exception


@freeze_time("2021-03-09")
def test_should_return_survey_result_on_success(sut: DbLoadSurveyResult):
    survey_result = sut.load("any_survey_id")
    expected = SurveyResultModel(
        survey_id="any_survey_id",
        question="any_question",
        answers=[
            dict(answer="any_answer", count=1, percent=40, image="any_image"),
            dict(answer="other_answer", count=2, percent=60, image="any_image"),
        ],
        date=datetime.utcnow(),
    )
    assert survey_result == expected
