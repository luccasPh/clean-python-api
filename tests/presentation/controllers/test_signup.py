import pytest
from mock import patch, MagicMock

from app.domain import AccountModel, AddAccount, AddAccountModel
from app.presentation import (
    SignUpController,
    HttpRequest,
    EmailValidator,
)


class EmailValidatorStub(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return True


class AddAccountStub(AddAccount):
    def add(self, data: AddAccountModel) -> AccountModel:
        fake_account = {
            "id": "valid_id",
            "name": "valid_name",
            "email": "valid_email@example.com",
            "hashed_password": "valid_password_hash",
        }
        return AccountModel(**fake_account)


@pytest.fixture
def sut():
    email_validator = EmailValidatorStub()
    add_account_stub = AddAccountStub()
    sut = SignUpController(email_validator, add_account_stub)
    yield sut


def test_should_400_if_no_name_provided(sut: SignUpController):
    request = HttpRequest(
        body={
            "email": "test@example.com",
            "password": "teste",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Missing param: name"


def test_should_400_if_no_email_provided(sut: SignUpController):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "password": "teste",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Missing param: email"


def test_should_400_if_no_password_provided(sut: SignUpController):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Missing param: password"


def test_should_400_if_no_password_confirmation_provided(sut: SignUpController):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "teste",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Missing param: password_confirmation"


def test_should_400_if_password_confirmation_fails(sut: SignUpController):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "invalid@example.com",
            "password": "test",
            "password_confirmation": "test_test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Invalid param: password_confirmation"


@patch.object(EmailValidatorStub, "is_valid")
def test_should_400_if_invalid_email_provided(
    mock_is_valid: MagicMock, sut: SignUpController
):
    mock_is_valid.return_value = False
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "invalid@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Invalid param: email"


@patch.object(EmailValidatorStub, "is_valid")
def test_should_call_email_validator_correct_value(
    mock_is_valid: MagicMock, sut: SignUpController
):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    sut.handle(request)
    mock_is_valid.assert_called_with("test@example.com")


@patch.object(EmailValidatorStub, "is_valid")
def test_should_500_if_email_validator_raise_exception(
    mock_is_valid: MagicMock, sut: SignUpController
):
    mock_is_valid.side_effect = Exception()
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    print(response)
    assert response.status_code == 500
    assert response.body["message"] == "Internal server error"


@patch.object(AddAccountStub, "add")
def test_should_call_add_account_correct_values(
    mock_add: MagicMock, sut: SignUpController
):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    sut.handle(request)
    expected = AddAccountModel(
        name="John Doe",
        email="test@example.com",
        password="test",
    )
    mock_add.assert_called_with(expected)


@patch.object(AddAccountStub, "add")
def test_should_500_if_add_account_raise_exception(
    mock_add: MagicMock, sut: SignUpController
):
    mock_add.side_effect = Exception()
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    print(response)
    assert response.status_code == 500
    assert response.body["message"] == "Internal server error"


def test_should_200_if_data_is_valid(sut: SignUpController):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    expected = {
        "id": "valid_id",
        "name": "valid_name",
        "email": "valid_email@example.com",
        "hashed_password": "valid_password_hash",
    }
    response = sut.handle(request)
    assert response.status_code == 200
    assert response.body == expected
