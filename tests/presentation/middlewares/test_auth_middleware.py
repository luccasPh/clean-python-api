import pytest

from app.presentation import AuthMiddleware, HttpRequest


@pytest.fixture
def sut():
    yield AuthMiddleware()


def test_should_return_403_if_no_access_token_exists_in_headers(sut: AuthMiddleware):
    http_response = sut.handle(HttpRequest(headers=None, body=None))
    assert http_response.status_code == 403
    assert http_response.body["message"] == "Access danied"
