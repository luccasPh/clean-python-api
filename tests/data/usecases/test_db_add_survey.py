import pytest
from mock import patch, MagicMock

from app.data import DbAddSurvey, AddSurveyRepo
from app.domain import AddSurveyModel, SurveyAnswer


class AddSurveyRepoStub(AddSurveyRepo):
    def add(self, data: AddSurveyModel):
        ...


@pytest.fixture
def sut():
    add_survey_repo_stub = AddSurveyRepoStub()
    yield DbAddSurvey(add_survey_repo_stub)


@patch.object(AddSurveyRepoStub, "add")
def test_should_call_add_on_add_survey_repo_correct_values(
    mock_add: MagicMock, sut: DbAddSurvey
):
    survey_data = AddSurveyModel(
        question="any_question",
        answers=[SurveyAnswer(image="any_image", answer="any_answer")],
    )
    sut.add(survey_data)
    mock_add.assert_called_with(survey_data)
