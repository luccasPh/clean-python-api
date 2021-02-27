import pytest
from mock import MagicMock, patch

from app.data import AddAccountRepo, DbAddAccount
from app.domain import AddAccountModel, AccountModel


class EncrypterStub:
    def encrypt(self, value: str) -> str:
        return "hashed_password"


class AddAccountRepoStub(AddAccountRepo):
    def add(self, data: AddAccountModel) -> AccountModel:
        fake_account = AccountModel(
            id="valid_id",
            name="valid_name",
            email="valid_email@example.com",
            password_hash="hashed_password",
        )
        return fake_account


@pytest.fixture
def sut():
    encrypter_stub = EncrypterStub()
    add_account_repo_stub = AddAccountRepoStub()
    sut = DbAddAccount(encrypter_stub, add_account_repo_stub)
    yield sut


@patch.object(EncrypterStub, "encrypt")
def test_should_call_encrypter_with_correct_value(
    mock_encrypt: MagicMock, sut: DbAddAccount
):
    account_data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )
    sut.add(account_data)
    mock_encrypt.assert_called_with("valid_password")


@patch.object(EncrypterStub, "encrypt")
def test_should_raise_if_encrypter_raise(mock_encrypt: MagicMock, sut: DbAddAccount):
    mock_encrypt.side_effect = Exception()
    account_data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.add(account_data)
    assert type(excinfo.value) is Exception


@patch.object(AddAccountRepoStub, "add")
def test_should_call_add_account_repo_with_correct_values(
    mock_add: MagicMock, sut: DbAddAccount
):
    account_data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )

    expected_call = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="hashed_password"
    )
    sut.add(account_data)
    mock_add.assert_called_with(expected_call)


@patch.object(AddAccountRepoStub, "add")
def test_should_raise_if_add_account_repo_raise(mock_add: MagicMock, sut: DbAddAccount):
    mock_add.side_effect = Exception()
    account_data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.add(account_data)
    assert type(excinfo.value) is Exception
