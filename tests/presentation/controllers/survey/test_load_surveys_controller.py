import pytest
from mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time

from app.presentation import LoadSurveysController, HttpRequest
from app.domain import SurveyModel, LoadSurveys


class LoadSurveysStub(LoadSurveys):
    def load(self) -> list[SurveyModel]:
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
