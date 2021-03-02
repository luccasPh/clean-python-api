import pytest
import mongomock
from mock import patch, MagicMock

from app.presentation import EmailValidation, EmailValidator


class EmailValidatorStub(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return True


@pytest.fixture
def sut():
    email_validator_stub = EmailValidatorStub()
    sut = EmailValidation("email", email_validator_stub)
    yield sut


@patch.object(EmailValidatorStub, "is_valid")
def test_should_call_email_validator_correct_value(
    mock_is_valid: MagicMock, sut: EmailValidation
):
    input = {
        "email": "test@example.com",
    }
    sut.validate(input)
    mock_is_valid.assert_called_with("test@example.com")


@patch.object(EmailValidatorStub, "is_valid")
def test_should_400_if_invalid_email_provided(
    mock_is_valid: MagicMock, sut: EmailValidation
):
    mock_is_valid.return_value = False
    input = {
        "email": "invalid@example.com",
    }
    result = sut.validate(input)
    assert result.args[0] == "Invalid param: email"


@patch("app.main.decorators.log.get_collection")
@patch.object(EmailValidatorStub, "is_valid")
def test_should_raise_if_email_validator_raise_exception(
    mock_is_valid: MagicMock, mock_get_collection: MagicMock, sut: EmailValidation
):
    mock_is_valid.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    input = {
        "email": "test@example.com",
    }

    with pytest.raises(Exception) as excinfo:
        assert sut.validate(input)
    assert type(excinfo.value) is Exception
