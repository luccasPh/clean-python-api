import pytest
import mongomock
from mock import patch, MagicMock

from app.domain import AddSurvey, AddSurveyModel
from app.presentation import AddSurveyController, HttpRequest, Validation


class ValidationStub(Validation):
    def validate(self, input):
        ...


class AddSurveyStub(AddSurvey):
    def add(self, data: AddSurveyModel):
        ...


@pytest.fixture
def sut():
    validation_stub = ValidationStub()
    add_survey_stub = AddSurveyStub()
    yield AddSurveyController(validation_stub, add_survey_stub)


@patch.object(ValidationStub, "validate")
def test_should_call_validation_correct_values(
    mock_validate: MagicMock, sut: AddSurveyController
):
    http_request = HttpRequest(
        body=dict(
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
        )
    )
    sut.handle(http_request)
    mock_validate.assert_called_with(http_request.body)


@patch.object(ValidationStub, "validate")
def test_return_400_if_validation_fails(
    mock_validate: MagicMock, sut: AddSurveyController
):
    mock_validate.return_value = Exception("Error on matrix")
    http_request = HttpRequest(
        body=dict(
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
        )
    )
    respose = sut.handle(http_request)
    assert respose.status_code == 400
    assert respose.body == {"message": "Error on matrix"}


@patch.object(AddSurveyStub, "add")
def test_should_call_add_survey_correct_values(
    mock_add: MagicMock, sut: AddSurveyController
):
    http_request = HttpRequest(
        body=dict(
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
        )
    )
    sut.handle(http_request)
    mock_add.assert_called_with(AddSurveyModel(**http_request.body))


@patch("app.main.decorators.log.get_collection")
@patch.object(AddSurveyStub, "add")
def test_should_500_if_add_survey_raise_exception(
    mock_add: MagicMock, mock_get_collection: MagicMock, sut: AddSurveyController
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


def test_return_204_on_success(sut: AddSurveyController):
    http_request = HttpRequest(
        body=dict(
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
        )
    )
    respose = sut.handle(http_request)
    assert respose.status_code == 204
    assert not respose.body
