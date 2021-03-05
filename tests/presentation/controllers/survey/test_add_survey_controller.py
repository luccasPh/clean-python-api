import pytest
from mock import patch, MagicMock

from app.presentation import AddSurveyController, HttpRequest, Validation


class ValidationStub(Validation):
    def validate(self, input):
        ...


@pytest.fixture
def sut():
    validation_stub = ValidationStub()
    yield AddSurveyController(validation_stub)


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
