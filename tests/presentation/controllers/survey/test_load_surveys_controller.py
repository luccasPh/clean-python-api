import pytest
import mongomock
from typing import Union
from mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time

from app.presentation import LoadSurveysController, HttpRequest
from app.domain import SurveyModel, LoadSurveys


class LoadSurveysStub(LoadSurveys):
    def load(self) -> Union[list[SurveyModel], None]:
        fake_survey_1 = dict(
            id="any_id",
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
            date=datetime.utcnow(),
        )
        fake_survey_2 = dict(
            id="other_id",
            question="other_question",
            answers=[dict(image="other_image", answer="other_answer")],
            date=datetime.utcnow(),
        )
        return [SurveyModel(**fake_survey_1), SurveyModel(**fake_survey_2)]


@pytest.fixture
def sut():
    load_surveys_stub = LoadSurveysStub()
    yield LoadSurveysController(load_surveys_stub)


@freeze_time("2021-03-09")
@patch.object(LoadSurveysStub, "load")
def test_should_load_surveys_calls_load(
    mock_load: MagicMock, sut: LoadSurveysController
):
    sut.handle(HttpRequest())
    mock_load.assert_called()


@freeze_time("2021-03-09")
def test_should_return_200_on_success(sut: LoadSurveysController):
    http_response = sut.handle(HttpRequest())
    expected = [
        dict(
            id="any_id",
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
            date=datetime.utcnow(),
        ),
        dict(
            id="other_id",
            question="other_question",
            answers=[dict(image="other_image", answer="other_answer")],
            date=datetime.utcnow(),
        ),
    ]
    assert http_response.status_code == 200
    assert http_response.body == expected


@patch("app.main.decorators.log.get_collection")
@patch.object(LoadSurveysStub, "load")
def test_should_500_if_load_surveys_raise_exception(
    mock_add: MagicMock, mock_get_collection: MagicMock, sut: LoadSurveysController
):
    mock_add.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    http_request = HttpRequest(
        body=dict(
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
        )
    )
    response = sut.handle(http_request)
    assert response.status_code == 500
    assert response.body["message"] == "Internal server error"
