import pytest
from typing import Union
from datetime import datetime
from mock import patch, MagicMock
from freezegun import freeze_time

from app.data import DbLoadSurveys, LoadSurveysRepo
from app.domain import SurveyModel


class LoadSurveysRepoStub(LoadSurveysRepo):
    def load_all(self) -> Union[list[SurveyModel], None]:
        return make_surveys()


def make_surveys() -> list[SurveyModel]:
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
    load_surveys_repo_stub = LoadSurveysRepoStub()
    yield DbLoadSurveys(load_surveys_repo_stub)


@patch.object(LoadSurveysRepoStub, "load_all")
def test_should_call_load_surveys_repo(mock_load_all: MagicMock, sut: DbLoadSurveys):
    sut.load()
    mock_load_all.assert_called()


@freeze_time("2021-03-09")
def test_should_return_a_list_of_surveys_on_success(sut: DbLoadSurveys):
    surveys = sut.load()
    assert surveys == make_surveys()


@patch.object(LoadSurveysRepoStub, "load_all")
def test_should_raise_exception_if_load_survey_repo_raise(
    mock_load_all: MagicMock, sut: DbLoadSurveys
):
    mock_load_all.side_effect = Exception("Error on matrix")
    with pytest.raises(Exception) as excinfo:
        assert sut.load()
    assert type(excinfo.value) is Exception
