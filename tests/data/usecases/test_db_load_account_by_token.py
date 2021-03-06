import pytest
from mock import patch, MagicMock

from app.data import Decrypter, DbLoadAccountByToken, LoadAccountByTokenRepo
from app.domain import AccountModel


class DecrypterStub(Decrypter):
    def decrypt(self, value: str) -> str:
        return "any_token"


class LoadAccountByTokenRepoStub(LoadAccountByTokenRepo):
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
    decrypter_stub = DecrypterStub()
    load_account_by_token_repo_stub = LoadAccountByTokenRepoStub()
    yield DbLoadAccountByToken(decrypter_stub, load_account_by_token_repo_stub)


@patch.object(DecrypterStub, "decrypt")
def test_should_call_decrypt_with_correct_value(
    mock_decrypt: MagicMock, sut: DbLoadAccountByToken
):
    sut.load("any_token", "any_role")
    mock_decrypt.assert_called_with("any_token")


@patch.object(DecrypterStub, "decrypt")
def test_should_return_none_if_decrypter_returns_none(
    mock_decrypt: MagicMock, sut: DbLoadAccountByToken
):
    mock_decrypt.return_value = None
    account = sut.load("any_token", "any_role")
    assert not account


@patch.object(LoadAccountByTokenRepoStub, "load_by_token")
def test_should_call_load_account_by_toke_correct_value(
    mock_load_by_token: MagicMock, sut: DbLoadAccountByToken
):
    sut.load("any_token", "any_role")
    mock_load_by_token.assert_called_with("any_token", "any_role")


@patch.object(LoadAccountByTokenRepoStub, "load_by_token")
def test_should_return_none_if_load_account_by_token_repo_returns_none(
    mock_load_by_token: MagicMock, sut: DbLoadAccountByToken
):
    mock_load_by_token.return_value = None
    account = sut.load("any_token", "any_role")
    assert not account
