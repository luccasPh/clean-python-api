import pytest
from mock import patch

from app.presentation import (
    SignUpController,
    Request,
    MissingParamError,
    InvalidParamError,
    EmailValidator,
)


class EmailValidatorStub(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return True


@pytest.fixture
def sut():
    email_validator = EmailValidatorStub()
    sut = SignUpController(email_validator)
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


@patch.object(EmailValidatorStub, "is_valid")
def test_should_400_if_invalid_email_provided(test_is_valid, sut):
    test_is_valid.return_value = False
    request = Request(
        body={
            "name": "John Doe",
            "email": "invalid@example.com",
            "password": "teste",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert type(response.body["message"]) == InvalidParamError
    assert response.body["message"].args[0] == "Invalid param: email"
