import pytest
import mongomock
from mock import patch, MagicMock
from jwt.exceptions import InvalidTokenError

from app.presentation import AuthMiddleware, HttpRequest
from app.domain import LoadAccountById, AccountModel


class LoadAccountByIdStub(LoadAccountById):
    def load(self, access_token: str, role: str = None) -> AccountModel:
        account = AccountModel(
            id="valid_id",
            name="valid_name",
            email="valid_email@example.com",
            hashed_password="hashed_password",
        )
        return account


@pytest.fixture
def sut():
    load_account_by_id_stub = LoadAccountByIdStub()
    yield AuthMiddleware(load_account_by_id_stub)


def test_should_return_403_if_no_access_token_exists_in_headers(sut: AuthMiddleware):
    http_response = sut.handle(HttpRequest(headers=None, body=None))
    assert http_response.status_code == 403
    assert http_response.body["message"] == "Access danied"


@patch.object(LoadAccountByIdStub, "load")
def test_should_calls_load_account_by_id_correct_values(
    mock_load: MagicMock, sut: AuthMiddleware
):
    sut.handle(HttpRequest(headers={"x-access-token": "any_token"}, body=None))
    mock_load.assert_called_with(access_token="any_token", role=None)


@patch.object(LoadAccountByIdStub, "load")
def test_should_return_403_if_load_account_by_id_returns_none(
    mock_load: MagicMock, sut: AuthMiddleware
):
    mock_load.return_value = None
    http_response = sut.handle(
        HttpRequest(headers={"x-access-token": "any_token"}, body=None)
    )
    assert http_response.status_code == 403


def test_should_return_200_if_load_account_by_id_returns_an_account(
    sut: AuthMiddleware,
):
    http_response = sut.handle(
        HttpRequest(headers={"x-access-token": "any_token"}, body=None)
    )
    assert http_response.status_code == 200
    assert http_response.body


@patch("app.main.decorators.log.get_collection")
@patch.object(LoadAccountByIdStub, "load")
def test_should_return_500_if_load_account_by_id_raise_exception(
    mock_load: MagicMock, mock_get_collection: MagicMock, sut: AuthMiddleware
):
    mock_load.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    http_response = sut.handle(
        HttpRequest(headers={"x-access-token": "any_token"}, body=None)
    )
    assert http_response.status_code == 500
    assert http_response.body["message"] == "Internal server error"


@patch("app.main.decorators.log.get_collection")
@patch.object(LoadAccountByIdStub, "load")
def test_should_return_401_if_load_account_by_id_raise_jwt_exception(
    mock_load: MagicMock, mock_get_collection: MagicMock, sut: AuthMiddleware
):
    mock_load.side_effect = InvalidTokenError()
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    http_response = sut.handle(
        HttpRequest(headers={"x-access-token": "any_token"}, body=None)
    )
    assert http_response.status_code == 401
    assert http_response.body["message"] == "Unauthorized"
