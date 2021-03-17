import pytest
from mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time
from typing import Union

from app.data import DbSaveSurveyResult, SaveSurveyResultRepo, LoadSurveyResultRepo
from app.domain import SurveyResultModel, SaveSurveyResultModel


class SaveSurveyResultRepoStub(SaveSurveyResultRepo):
    def save(self, data: SaveSurveyResultModel):
        ...


class LoadSurveyResultRepoStub(LoadSurveyResultRepo):
    def load_by_survey_id(self, survey_id) -> Union[SurveyResultModel, None]:
        data = dict(
            survey_id="any_survey_id",
            question="any_question",
            answers=[
                dict(answer="any_answer", count=1, percent=40, image="any_image"),
                dict(answer="other_answer", count=2, percent=60, image="any_image"),
            ],
            date=datetime.utcnow(),
        )
        return SurveyResultModel(**data)


@pytest.fixture
def sut():
    load_survey_result_repo_stub = LoadSurveyResultRepoStub()
    save_survey_result_repo_stub = SaveSurveyResultRepoStub()
    yield DbSaveSurveyResult(save_survey_result_repo_stub, load_survey_result_repo_stub)


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


@patch.object(SaveSurveyResultRepoStub, "save")
def test_should_raise_exception_if_load_survey_repo_raise(
    mock_save: MagicMock, sut: DbSaveSurveyResult
):
    mock_save.side_effect = Exception("Error on matrix")
    survey_result = SaveSurveyResultModel(
        survey_id="any_survey_id", account_id="any_account_id", answer="any_answer"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.save(survey_result)
    assert type(excinfo.value) is Exception


@freeze_time("2021-03-09")
@patch.object(LoadSurveyResultRepoStub, "load_by_survey_id")
def test_should_call_load_survey_result_repo_correct_values(
    load_by_survey_id: MagicMock, sut: DbSaveSurveyResult
):
    survey_result = SaveSurveyResultModel(
        survey_id="any_survey_id", account_id="any_account_id", answer="any_answer"
    )
    sut.save(survey_result)
    load_by_survey_id.assert_called_with("any_survey_id")


@patch.object(LoadSurveyResultRepoStub, "load_by_survey_id")
def test_should_raise_exception_if_load_survey_result_repo_raise(
    load_by_survey_id: MagicMock, sut: DbSaveSurveyResult
):
    load_by_survey_id.side_effect = Exception("Error on matrix")
    survey_result = SaveSurveyResultModel(
        survey_id="any_survey_id", account_id="any_account_id", answer="any_answer"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.save(survey_result)
    assert type(excinfo.value) is Exception


@freeze_time("2021-03-09")
def test_should_return_survey_result_on_success(sut: DbSaveSurveyResult):
    data = SaveSurveyResultModel(
        survey_id="any_survey_id", account_id="any_account_id", answer="any_answer"
    )
    survey_result = sut.save(data)
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
