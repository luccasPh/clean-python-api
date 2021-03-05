import pytest
import mongomock
from mock import patch, MagicMock

from app.validations import EmailValidation, EmailValidator, EmailAvailability


class EmailValidatorStub(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return True


class EmailAvailabilityStub(EmailAvailability):
    def load_by_email(self, email: str):
        return None


@pytest.fixture
def sut():
    email_validator_stub = EmailValidatorStub()
    load_account_by_email_repo_stub = EmailAvailabilityStub()
    sut = EmailValidation(
        "email", email_validator_stub, load_account_by_email_repo_stub
    )
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
def test_should_return_invalid_param_if_invalid_email_provided(
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


@patch.object(EmailAvailabilityStub, "load_by_email")
def test_should_call_load_accout_by_email_correct_value(
    mock_load_by_email: MagicMock, sut: EmailValidation
):
    input = {
        "email": "test@example.com",
    }
    sut.validate(input)
    mock_load_by_email.assert_called_with("test@example.com")


@patch("app.main.decorators.log.get_collection")
@patch.object(EmailAvailabilityStub, "load_by_email")
def test_should_raise_if_load_account_by_email_raise_exception(
    mock_load_by_email: MagicMock, mock_get_collection: MagicMock, sut: EmailValidation
):
    mock_load_by_email.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    input = {
        "email": "test@example.com",
    }

    with pytest.raises(Exception) as excinfo:
        assert sut.validate(input)
    assert type(excinfo.value) is Exception


@patch.object(EmailAvailabilityStub, "load_by_email")
def test_should_return_email_in_used_if_email_used_provided(
    mock_load_by_email: MagicMock, sut: EmailValidation
):
    mock_load_by_email.return_value = "Account"
    input = {
        "email": "email_used@example.com",
    }
    result = sut.validate(input)
    assert result.args[0] == "The received email is already in use"
