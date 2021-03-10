import pytest
from typing import Union
from datetime import datetime
from mock import patch, MagicMock

# from freezegun import freeze_time

from app.data import DbLoadSurveyById, LoadSurveyByIdRepo
from app.domain import SurveyModel


class LoadSurveyByIdRepoStub(LoadSurveyByIdRepo):
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
    load_survey_by_id_repo_stub = LoadSurveyByIdRepoStub()
    yield DbLoadSurveyById(load_survey_by_id_repo_stub)


@patch.object(LoadSurveyByIdRepoStub, "load_by_id")
def test_should_call_load_survey_by_id_repo_with_value(
    mock_load_by_id: MagicMock, sut: DbLoadSurveyById
):
    sut.load_by_id("any_id")
    mock_load_by_id.assert_called_with("any_id")


# @freeze_time("2021-03-09")
# def test_should_return_a_list_of_surveys_on_success(sut: DbLoadSurveyById):
#     surveys = sut.load()
#     assert surveys == make_surveys()


# @patch.object(LoadSurveyByIdRepoStub, "load_by_id")
# def test_should_raise_exception_if_load_survey_repo_raise(
#     mock_load_by_id: MagicMock, sut: DbLoadSurveyById
# ):
#     mock_load_by_id.side_effect = Exception("Error on matrix")
#     with pytest.raises(Exception) as excinfo:
#         assert sut.load()
#     assert type(excinfo.value) is Exception
