import pytest
from mock import patch

from app.domain import AccountModel, AddAccount, AddAccountModel
from app.presentation import (
    SignUpController,
    Request,
    MissingParamError,
    InvalidParamError,
    EmailValidator,
    ServerError,
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
            "password_hash": "valid_password_hash",
        }
        return AccountModel(**fake_account)


@pytest.fixture
def sut():
    email_validator = EmailValidatorStub()
    add_account_stub = AddAccountStub()
    sut = SignUpController(email_validator, add_account_stub)
    yield sut


def test_should_400_if_no_name_provided(sut: SignUpController):
    request = Request(
        body={
            "email": "test@example.com",
            "password": "teste",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert type(response.body["message"]) == MissingParamError
    assert response.body["message"].args[0] == "Missing param: name"


def test_should_400_if_no_email_provided(sut: SignUpController):
    request = Request(
        body={
            "name": "John Doe",
            "password": "teste",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert type(response.body["message"]) == MissingParamError
    assert response.body["message"].args[0] == "Missing param: email"


def test_should_400_if_no_password_provided(sut: SignUpController):
    request = Request(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert type(response.body["message"]) == MissingParamError
    assert response.body["message"].args[0] == "Missing param: password"


def test_should_400_if_no_password_confirmation_provided(sut: SignUpController):
    request = Request(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "teste",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert type(response.body["message"]) == MissingParamError
    assert response.body["message"].args[0] == "Missing param: password_confirmation"


def test_should_400_if_password_confirmation_fails(sut: SignUpController):
    request = Request(
        body={
            "name": "John Doe",
            "email": "invalid@example.com",
            "password": "test",
            "password_confirmation": "test_test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert type(response.body["message"]) == InvalidParamError
    assert response.body["message"].args[0] == "Invalid param: password_confirmation"


@patch.object(EmailValidatorStub, "is_valid")
def test_should_400_if_invalid_email_provided(test_is_valid, sut: SignUpController):
    test_is_valid.return_value = False
    request = Request(
        body={
            "name": "John Doe",
            "email": "invalid@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert type(response.body["message"]) == InvalidParamError
    assert response.body["message"].args[0] == "Invalid param: email"


@patch.object(EmailValidatorStub, "is_valid")
def test_should_call_email_validator_correct_value(
    test_is_valid, sut: SignUpController
):
    request = Request(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    sut.handle(request)
    test_is_valid.assert_called_with("test@example.com")


@patch.object(EmailValidatorStub, "is_valid")
def test_should_500_if_email_validator_raise_exception(
    test_is_valid, sut: SignUpController
):
    test_is_valid.side_effect = Exception()
    request = Request(
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
    assert type(response.body["message"]) == ServerError
    assert response.body["message"].args[0] == "Internal server error"


@patch.object(AddAccountStub, "add")
def test_should_call_add_account_correct_values(test_add, sut: SignUpController):
    request = Request(
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
    test_add.assert_called_with(expected)


@patch.object(AddAccountStub, "add")
def test_should_500_if_add_account_raise_exception(test_add, sut: SignUpController):
    test_add.side_effect = Exception()
    request = Request(
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
    assert type(response.body["message"]) == ServerError
    assert response.body["message"].args[0] == "Internal server error"


def test_should_200_if_data_is_valid(sut: SignUpController):
    request = Request(
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
        "password_hash": "valid_password_hash",
    }
    response = sut.handle(request)
    assert response.status_code == 200
    assert response.body == expected
