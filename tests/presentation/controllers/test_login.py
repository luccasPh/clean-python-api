import pytest

from app.presentation import LoginController, HttpRequest


@pytest.fixture
def sut():
    sut = LoginController()
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
