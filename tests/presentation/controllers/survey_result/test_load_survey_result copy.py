import pytest
from datetime import datetime
from typing import Union
from mock import patch, MagicMock

from app.presentation import LoadSurveyResultController, HttpRequest
from app.domain import LoadSurveyById, SurveyModel


class LoadSurveyByIdStub(LoadSurveyById):
    def load_by_id(self, id: str) -> Union[SurveyModel, None]:
        fake_survey = dict(
            id="any_id",
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
            date=datetime.utcnow(),
        )
        return SurveyModel(**fake_survey)


@pytest.fixture
def sut():
    load_survey_by_id_stub = LoadSurveyByIdStub()
    yield LoadSurveyResultController(load_survey_by_id_stub)


@patch.object(LoadSurveyByIdStub, "load_by_id")
def test_should_calls_load_survey_by_id_with_value(
    mock_load_by_id: MagicMock, sut: LoadSurveyResultController
):
    sut.handle(HttpRequest(params=dict(survey_id="any_id")))
    mock_load_by_id.assert_called_with("any_id")


@patch.object(LoadSurveyByIdStub, "load_by_id")
def test_should_403_if_load_survey_by_id_returns_none(
    mock_load_by_id: MagicMock, sut: LoadSurveyResultController
):
    mock_load_by_id.return_value = None
    http_response = sut.handle(HttpRequest(params=dict(survey_id="any_id")))
    assert http_response.status_code == 403
    assert http_response.body["message"] == "Invalid param: survey_id"


@patch.object(LoadSurveyByIdStub, "load_by_id")
def test_should_500_if_load_survey_by_id_raise_exception(
    mock_load_by_id: MagicMock, sut: LoadSurveyResultController
):
    mock_load_by_id.side_effect = Exception("Error on matrix")
    http_response = sut.handle(HttpRequest(params=dict(survey_id="any_id")))
    assert http_response.status_code == 500
    assert http_response.body["message"] == "Internal server error"
