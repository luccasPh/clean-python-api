import pytest
import mongomock
from datetime import datetime
from typing import Union
from mock import patch, MagicMock
from freezegun import freeze_time

from app.presentation import SaveSurveyResultController, HttpRequest
from app.domain import (
    LoadSurveyById,
    SurveyModel,
    SaveSurveyResult,
    SaveSurveyResultModel,
    SurveyResultModel,
)


class LoadSurveyByIdStub(LoadSurveyById):
    def load_by_id(self, id: str) -> Union[SurveyModel, None]:
        fake_survey = dict(
            id="any_id",
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
            date=datetime.utcnow(),
        )
        return SurveyModel(**fake_survey)


class SaveSurveyResultStub(SaveSurveyResult):
    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        survey_result = dict(
            id="any_id",
            survey_id=data.survey_id,
            account_id=data.account_id,
            answer=data.answer,
            date=datetime.utcnow(),
        )
        return SurveyResultModel(**survey_result)


@pytest.fixture
def sut():
    load_survey_by_id_stub = LoadSurveyByIdStub()
    save_survey_result_stub = SaveSurveyResultStub()
    yield SaveSurveyResultController(load_survey_by_id_stub, save_survey_result_stub)


@patch.object(LoadSurveyByIdStub, "load_by_id")
def test_should_calls_load_survey_by_id_with_values(
    mock_load_by_id: MagicMock, sut: SaveSurveyResultController
):
    sut.handle(
        HttpRequest(
            params=dict(survey_id="any_id"),
            body=dict(answer="any_answer"),
            account_id="any_account_id",
        )
    )
    mock_load_by_id.assert_called_with("any_id")


@patch.object(LoadSurveyByIdStub, "load_by_id")
def test_should_403_if_load_survey_by_id_returns_none(
    mock_load_by_id: MagicMock, sut: SaveSurveyResultController
):
    mock_load_by_id.return_value = None
    http_response = sut.handle(
        HttpRequest(
            params=dict(survey_id="any_id"),
            body=dict(answer="any_answer"),
            account_id="any_account_id",
        )
    )
    assert http_response.status_code == 403
    assert http_response.body["message"] == "Invalid param: survey_id"


@patch("app.main.decorators.log.get_collection")
@patch.object(LoadSurveyByIdStub, "load_by_id")
def test_should_500_if_load_survey_by_id_raise_exception(
    mock_load_by_id: MagicMock,
    mock_get_collection: MagicMock,
    sut: SaveSurveyResultController,
):
    mock_load_by_id.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    http_response = sut.handle(
        HttpRequest(
            params=dict(survey_id="any_id"),
            body=dict(answer="any_answer"),
            account_id="any_account_id",
        )
    )
    assert http_response.status_code == 500
    assert http_response.body["message"] == "Internal server error"


def test_should_403_if_an_invalid_answer_is_provided(sut: SaveSurveyResultController):
    http_response = sut.handle(
        HttpRequest(
            params=dict(survey_id="any_id"),
            body=dict(answer="invalid_answer"),
            account_id="any_account_id",
        )
    )
    assert http_response.status_code == 403
    assert http_response.body["message"] == "Invalid param: answer"


@patch("app.main.decorators.log.get_collection")
@patch.object(SaveSurveyResultStub, "save")
def test_should_calls_save_survey_result_with_values(
    mock_save: MagicMock,
    mock_get_collection: MagicMock,
    sut: SaveSurveyResultController,
):
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    sut.handle(
        HttpRequest(
            params=dict(survey_id="any_id"),
            body=dict(answer="any_answer"),
            account_id="any_account_id",
        )
    )
    mock_save.assert_called_with(
        SaveSurveyResultModel(
            survey_id="any_id", account_id="any_account_id", answer="any_answer"
        )
    )


@patch("app.main.decorators.log.get_collection")
@patch.object(SaveSurveyResultStub, "save")
def test_should_500_if_save_survey_result_raise_exception(
    mock_save: MagicMock,
    mock_get_collection: MagicMock,
    sut: SaveSurveyResultController,
):
    mock_save.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    http_response = sut.handle(
        HttpRequest(
            params=dict(survey_id="any_id"),
            body=dict(answer="any_answer"),
            account_id="any_account_id",
        )
    )
    assert http_response.status_code == 500
    assert http_response.body["message"] == "Internal server error"


@freeze_time("2021-03-09")
def test_should_200_on_success(
    sut: SaveSurveyResultController,
):
    http_response = sut.handle(
        HttpRequest(
            params=dict(survey_id="any_survey_id"),
            body=dict(answer="any_answer"),
            account_id="any_account_id",
        )
    )
    assert http_response.status_code == 200
    assert http_response.body == dict(
        id="any_id",
        survey_id="any_survey_id",
        account_id="any_account_id",
        answer="any_answer",
        date=datetime.utcnow(),
    )
