import pytest
from mock import patch, MagicMock

from app.domain import AccountModel, AuthenticationModel
from app.data import (
    LoadAccountByEmailRepo,
    DbAuthentication,
    HashComparer,
    Encrypter,
)


class LoadAccountByEmailRepoStub(LoadAccountByEmailRepo):
    def load_by_email(self, email: str) -> AccountModel:
        account = AccountModel(
            id="valid_id",
            name="valid_name",
            email="valid_email",
            hashed_password="hashed_password",
        )
        return account


class HashComparerStub(HashComparer):
    def compare(self, value: str, hash: str) -> bool:
        return True


class EncrypterStub(Encrypter):
    def encrypt(self, value: str) -> str:
        return "access_token"


@pytest.fixture
def sut():
    load_account_by_email_repo_stub = LoadAccountByEmailRepoStub()
    hash_comparer_stub = HashComparerStub()
    token_comparer_stub = EncrypterStub()
    return DbAuthentication(
        load_account_by_email_repo_stub,
        hash_comparer_stub,
        token_comparer_stub,
    )


@patch.object(LoadAccountByEmailRepoStub, "load_by_email")
def test_should_call_load_accout_by_email_correct_value(
    mock_load_by_email: MagicMock, sut: DbAuthentication
):
    sut.auth(AuthenticationModel(email="valid_email@example.com", password="password"))
    mock_load_by_email.assert_called_with("valid_email@example.com")


@patch.object(LoadAccountByEmailRepoStub, "load_by_email")
def test_should_raise_exception_if_loader_accout_by_email_raise(
    mock_load_by_email: MagicMock, sut: DbAuthentication
):
    mock_load_by_email.side_effect = Exception("Error on matrix")
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.auth(authentication)
    assert type(excinfo.value) is Exception


@patch.object(LoadAccountByEmailRepoStub, "load_by_email")
def test_should_return_none_if_load_account_by_email_returns_none(
    mock_load_by_email: MagicMock, sut: DbAuthentication
):
    mock_load_by_email.return_value = None
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    access_token = sut.auth(authentication)
    assert not access_token


@patch.object(HashComparerStub, "compare")
def test_should_call_hash_compare_correct_values(
    mock_compare: MagicMock, sut: DbAuthentication
):
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    sut.auth(authentication)
    mock_compare.assert_called_with("valid_password", "hashed_password")


@patch.object(HashComparerStub, "compare")
def test_should_raise_exception_if__hash_compare_raise(
    mock_compare: MagicMock, sut: DbAuthentication
):
    mock_compare.side_effect = Exception("Error on matrix")
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.auth(authentication)
    assert type(excinfo.value) is Exception


@patch.object(HashComparerStub, "compare")
def test_should_return_none_if_hash_compare_returns_false(
    mock_compare: MagicMock, sut: DbAuthentication
):
    mock_compare.return_value = False
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    access_token = sut.auth(authentication)
    assert not access_token


@patch.object(EncrypterStub, "encrypt")
def test_should_call_encrypter_correct_value(
    mock_encrypt: MagicMock, sut: DbAuthentication
):
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    sut.auth(authentication)
    mock_encrypt.assert_called_with("valid_id")


@patch.object(EncrypterStub, "encrypt")
def test_should_raise_exception_if_encrypter_raise(
    mock_encrypt: MagicMock, sut: DbAuthentication
):
    mock_encrypt.side_effect = Exception("Error on matrix")
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.auth(authentication)
    assert type(excinfo.value) is Exception


def test_should_return_an_access_token_on_success(sut: DbAuthentication):
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    access_token = sut.auth(authentication)
    assert access_token == "access_token"
