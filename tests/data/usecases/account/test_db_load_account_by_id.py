import pytest
from mock import patch, MagicMock

from app.data import Decrypter, DbLoadAccountById, LoadAccountByIdRepo
from app.domain import AccountModel


class DecrypterStub(Decrypter):
    def decrypt(self, value: str) -> str:
        return "any_id"


class LoadAccountByIdRepoStub(LoadAccountByIdRepo):
    def load_by_id(self, id: str, role: str = None) -> AccountModel:
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
    load_account_by_id_repo_stub = LoadAccountByIdRepoStub()
    yield DbLoadAccountById(decrypter_stub, load_account_by_id_repo_stub)


@patch.object(DecrypterStub, "decrypt")
def test_should_call_decrypt_with_correct_value(
    mock_decrypt: MagicMock, sut: DbLoadAccountById
):
    sut.load("any_id", "any_role")
    mock_decrypt.assert_called_with("any_id")


@patch.object(DecrypterStub, "decrypt")
def test_should_return_none_if_decrypter_returns_none(
    mock_decrypt: MagicMock, sut: DbLoadAccountById
):
    mock_decrypt.return_value = None
    account = sut.load("any_id", "any_role")
    assert not account


@patch.object(DecrypterStub, "decrypt")
def test_should_raise_exception_if_decrypter_raise(
    mock_decrypt: MagicMock, sut: DbLoadAccountById
):
    mock_decrypt.side_effect = Exception("Error on matrix")
    with pytest.raises(Exception) as excinfo:
        assert sut.load("any_id", "any_role")
    assert type(excinfo.value) is Exception


@patch.object(LoadAccountByIdRepoStub, "load_by_id")
def test_should_call_load_account_by_id_correct_value(
    mock_load_by_id: MagicMock, sut: DbLoadAccountById
):
    sut.load("any_id", "any_role")
    mock_load_by_id.assert_called_with("any_id", "any_role")


@patch.object(LoadAccountByIdRepoStub, "load_by_id")
def test_should_return_none_if_load_account_by_id_repo_returns_none(
    mock_load_by_id: MagicMock, sut: DbLoadAccountById
):
    mock_load_by_id.return_value = None
    account = sut.load("any_id", "any_role")
    assert not account


def test_should_return_an_account_on_success(sut: DbLoadAccountById):
    account = sut.load("any_id", "any_role")
    assert account
    assert account.id == "valid_id"
    assert account.name == "valid_name"
    assert account.email == "valid_email@example.com"
    assert account.hashed_password == "hashed_password"


@patch.object(LoadAccountByIdRepoStub, "load_by_id")
def test_should_raise_exception_if_load_account_by_id_raise(
    mock_load_by_id: MagicMock, sut: DbLoadAccountById
):
    mock_load_by_id.side_effect = Exception("Error on matrix")
    with pytest.raises(Exception) as excinfo:
        assert sut.load("any_id", "any_role")
    assert type(excinfo.value) is Exception
