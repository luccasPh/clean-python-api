import pytest
from mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time
from typing import Union

from app.data import DbLoadSurveyResult, LoadSurveyResultRepo, LoadSurveyByIdRepo
from app.domain import SurveyResultModel, SurveyModel


class LoadSurveyResultRepoStub(LoadSurveyResultRepo):
    def load_by_survey_id(self, survey_id: str) -> Union[SurveyResultModel, None]:
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


class LoadSurveyByIdRepoStub(LoadSurveyByIdRepo):
    def load_by_id(self, id: str) -> Union[SurveyModel, None]:
        return make_fake_survey()


def make_fake_survey() -> SurveyModel:
    fake_survey = dict(
        id="any_survey_id",
        question="any_question",
        answers=[
            dict(image="any_image", answer="any_answer"),
            dict(image="any_image", answer="other_answer"),
        ],
        date=datetime.utcnow(),
    )
    return SurveyModel(**fake_survey)


@pytest.fixture
def sut():
    load_survey_result_repo_stub = LoadSurveyResultRepoStub()
    load_survey_by_id_repo_stub = LoadSurveyByIdRepoStub()
    yield DbLoadSurveyResult(load_survey_result_repo_stub, load_survey_by_id_repo_stub)


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
@patch.object(LoadSurveyByIdRepoStub, "load_by_id")
@patch.object(LoadSurveyResultRepoStub, "load_by_survey_id")
def test_should_call_load_survey_by_id_repo_if_load_survey_result_repo_returns_none(
    load_by_survey_id: MagicMock, load_by_id: MagicMock, sut: DbLoadSurveyResult
):
    load_by_survey_id.return_value = None
    load_by_id.return_value = make_fake_survey()
    sut.load("any_survey_id")
    load_by_id.assert_called_with("any_survey_id")


@freeze_time("2021-03-09")
@patch.object(LoadSurveyResultRepoStub, "load_by_survey_id")
def test_should_return_survey_result_answers_count_0_if_load_survey_result_repo_returns_none(
    load_by_survey_id: MagicMock, sut: DbLoadSurveyResult
):
    load_by_survey_id.return_value = None
    survey_result = sut.load("any_survey_id")
    expected = SurveyResultModel(
        survey_id="any_survey_id",
        question="any_question",
        answers=[
            dict(answer="any_answer", count=0, percent=0, image="any_image"),
            dict(answer="other_answer", count=0, percent=0, image="any_image"),
        ],
        date=datetime.utcnow(),
    )
    assert survey_result == expected


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
