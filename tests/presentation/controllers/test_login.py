import pytest
from mock import patch, MagicMock

from app.presentation import LoginController, HttpRequest, EmailValidator


class EmailValidatorStub(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return True


@pytest.fixture
def sut():
    email_validator_stub = EmailValidatorStub()
    sut = LoginController(email_validator_stub)
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
def test_should_call_email_validator_correct_value(
    mock_is_valid: MagicMock, sut: LoginController
):
    request = HttpRequest(body=dict(email="email@example.com", password="password"))
    sut.handle(request)
    mock_is_valid.assert_called_with("email@example.com")
