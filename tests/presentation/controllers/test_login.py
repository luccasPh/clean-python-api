import pytest
import mongomock
from mock import patch, MagicMock

from app.domain import Authentication, AuthenticationModel
from app.presentation import (
    LoginController,
    HttpRequest,
    Validation,
    MissingParamError,
)


class AuthenticationStub(Authentication):
    def auth(self, authentication: AuthenticationModel) -> str:
        return "access_token"


class ValidationStub(Validation):
    def validate(self, input):
        ...


@pytest.fixture
def sut():
    authentication_stub = AuthenticationStub()
    validation_stub = ValidationStub()
    sut = LoginController(authentication_stub, validation_stub)
    yield sut


@patch.object(AuthenticationStub, "auth")
def test_should_call_authentication_correct_value(
    mock_auth: MagicMock, sut: LoginController
):
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    sut.handle(request)
    mock_auth.assert_called_with(AuthenticationModel(**request.body))


@patch.object(AuthenticationStub, "auth")
def test_should_401_if_invalid_credentials_are_provided(
    mock_auth: MagicMock, sut: LoginController
):
    mock_auth.return_value = None
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    response = sut.handle(request)
    assert response.status_code == 401
    assert response.body["message"] == "Unauthorized"


@patch("app.main.decorators.log.get_collection")
@patch.object(AuthenticationStub, "auth")
def test_should_500_if_authentication__raise_exception(
    mock_auth: MagicMock, mock_get_collection: MagicMock, sut: LoginController
):
    mock_auth.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    response = sut.handle(request)
    assert response.status_code == 500
    assert response.body["message"] == "Internal server error"


def test_should_200_if_valid_credentials_are_provided(sut: LoginController):
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    response = sut.handle(request)
    assert response.status_code == 200
    assert response.body["access_token"] == "access_token"


@patch.object(ValidationStub, "validate")
def test_should_call_validation_correct_value(
    mock_validate: MagicMock, sut: LoginController
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
    mock_validate.assert_called_with(request.body)


@patch.object(ValidationStub, "validate")
def test_should_400_if_validation_returns_error(
    mock_validate: MagicMock, sut: LoginController
):
    mock_validate.return_value = MissingParamError("any_field")
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body == dict(message="Missing param: any_field")
