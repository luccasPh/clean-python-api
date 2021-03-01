import pytest
import mongomock
from mock import patch, MagicMock

from app.presentation import LoginController, HttpRequest, EmailValidator
from app.domain import Authentication


class EmailValidatorStub(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return True


class AuthenticationStub(Authentication):
    def auth(self, valid_data: dict) -> str:
        return "access_token"


@pytest.fixture
def sut():
    email_validator_stub = EmailValidatorStub()
    authentication_stub = AuthenticationStub()
    sut = LoginController(email_validator_stub, authentication_stub)
    yield sut


def test_should_400_if_no_email_provided(sut: LoginController):
    request = HttpRequest(body=dict(password="password"))
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Missing param: email"


def test_should_400_if_no_password_provided(sut: LoginController):
    request = HttpRequest(body=dict(email="email@example.com"))
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Missing param: password"


@patch.object(EmailValidatorStub, "is_valid")
def test_should_400_if_an_invalid_email(mock_is_valid: MagicMock, sut: LoginController):
    mock_is_valid.return_value = False
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body["message"] == "Invalid param: email"


@patch.object(EmailValidatorStub, "is_valid")
def test_should_call_email_validator_correct_value(
    mock_is_valid: MagicMock, sut: LoginController
):
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    sut.handle(request)
    mock_is_valid.assert_called_with("email@example.com")


@patch("app.main.decorators.log.get_collection")
@patch.object(EmailValidatorStub, "is_valid")
def test_should_500_if_email_validator_raise_exception(
    mock_is_valid: MagicMock, mock_get_collection: MagicMock, sut: LoginController
):
    mock_is_valid.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    response = sut.handle(request)
    assert response.status_code == 500
    assert response.body["message"] == "Internal server error"


@patch.object(AuthenticationStub, "auth")
def test_should_call_authentication_correct_value(
    mock_auth: MagicMock, sut: LoginController
):
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    sut.handle(request)
    mock_auth.assert_called_with({"email": "email@example.com", "password": "password"})


@patch.object(AuthenticationStub, "auth")
def test_should_401_if_invalid_credentials_are_provided(
    mock_auth: MagicMock, sut: LoginController
):
    mock_auth.return_value = None
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    response = sut.handle(request)
    assert response.status_code == 401
    assert response.body["message"] == "Unauthorized"
