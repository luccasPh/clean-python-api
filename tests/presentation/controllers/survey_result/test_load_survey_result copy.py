import pytest
from datetime import datetime
from typing import Union
from mock import patch, MagicMock

from app.presentation import LoadSurveyResultController, HttpRequest
from app.domain import LoadSurveyById, SurveyModel, LoadSurveyResult, SurveyResultModel


class LoadSurveyByIdStub(LoadSurveyById):
    def load_by_id(self, id: str) -> Union[SurveyModel, None]:
        fake_survey = dict(
            id="any_id",
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
            date=datetime.utcnow(),
        )
        return SurveyModel(**fake_survey)


class LoadSurveyResultStub(LoadSurveyResult):
    def load(self, survey_id: str) -> SurveyResultModel:
        fake_survey_result = dict(
            survey_id=survey_id,
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
    load_survey_by_id_stub = LoadSurveyByIdStub()
    load_survey_result_stub = LoadSurveyResultStub()
    yield LoadSurveyResultController(load_survey_by_id_stub, load_survey_result_stub)


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


@patch.object(LoadSurveyResultStub, "load")
def test_should_call_load_survey_result_with_correct_value(
    mock_load: MagicMock, sut: LoadSurveyResultController
):
    mock_load.side_effect = Exception("Error on matrix")
    sut.handle(HttpRequest(params=dict(survey_id="any_id")))
    mock_load.assert_called_with("any_id")
