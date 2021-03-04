import pytest
from mock import MagicMock, patch

from app.data import AddAccountRepo, DbAddAccount
from app.domain import AddAccountModel


class HasherStub:
    def hash(self, value: str) -> str:
        return "hashed_password"


class AddAccountRepoStub(AddAccountRepo):
    def add(self, data: AddAccountModel):
        ...


@pytest.fixture
def sut():
    hasher_stub = HasherStub()
    add_account_repo_stub = AddAccountRepoStub()
    sut = DbAddAccount(hasher_stub, add_account_repo_stub)
    yield sut


@patch.object(HasherStub, "hash")
def test_should_call_Hasher_with_correct_value(mock_hash: MagicMock, sut: DbAddAccount):
    account_data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )
    sut.add(account_data)
    mock_hash.assert_called_with("valid_password")


@patch.object(HasherStub, "hash")
def test_should_raise_if_Hasher_raise(mock_hash: MagicMock, sut: DbAddAccount):
    mock_hash.side_effect = Exception()
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
