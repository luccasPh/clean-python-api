import pytest
from mock import patch, MagicMock

from app.presentation import AuthMiddleware, HttpRequest
from app.domain import LoadAccountByToken, AccountModel


class LoadAccountByTokenStub(LoadAccountByToken):
    def load_by_token(self, access_token: str, role: str = None) -> AccountModel:
        account = AccountModel(
            id="valid_id",
            name="valid_name",
            email="valid_email@example.com",
            hashed_password="hashed_password",
        )
        return account


@pytest.fixture
def sut():
    load_account_by_token_stub = LoadAccountByTokenStub()
    yield AuthMiddleware(load_account_by_token_stub)


def test_should_return_403_if_no_access_token_exists_in_headers(sut: AuthMiddleware):
    http_response = sut.handle(HttpRequest(headers=None, body=None))
    assert http_response.status_code == 403
    assert http_response.body["message"] == "Access danied"


@patch.object(LoadAccountByTokenStub, "load_by_token")
def test_should_calls_load_account_by_token_correct_value(
    mock_load_by_token: MagicMock, sut: AuthMiddleware
):
    sut.handle(HttpRequest(headers={"x-access-token": "any_token"}, body=None))
    mock_load_by_token.assert_called_with(access_token="any_token")


@patch.object(LoadAccountByTokenStub, "load_by_token")
def test_should_return_403_if_load_account_by_token_returns_none(
    mock_load_by_token: MagicMock, sut: AuthMiddleware
):
    mock_load_by_token.return_value = None
    http_response = sut.handle(
        HttpRequest(headers={"x-access-token": "any_token"}, body=None)
    )
    assert http_response.status_code == 403


def test_should_return_200_if_load_account_by_token_returns_an_account(
    sut: AuthMiddleware,
):
    http_response = sut.handle(
        HttpRequest(headers={"x-access-token": "any_token"}, body=None)
    )
    assert http_response.status_code == 200
    assert http_response.body
