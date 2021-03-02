import pytest
from mock import patch, MagicMock

from app.domain import AccountModel, AuthenticationModel
from app.data import LoadAccountByEmailRepo, DbAuthentication, HashComparer


class LoadAccountByEmailRepoStub(LoadAccountByEmailRepo):
    def load(self, email: str) -> AccountModel:
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


@pytest.fixture
def sut():
    load_account_by_email_repo_stub = LoadAccountByEmailRepoStub()
    hash_comparer_stub = HashComparerStub()
    return DbAuthentication(load_account_by_email_repo_stub, hash_comparer_stub)


@patch.object(LoadAccountByEmailRepoStub, "load")
def test_should_call_loader_accout_by_email_correct_value(
    mock_load_account_by_email_repo_stub: MagicMock, sut: DbAuthentication
):
    sut.auth(AuthenticationModel(email="valid_email@example.com", password="password"))
    mock_load_account_by_email_repo_stub.assert_called_with("valid_email@example.com")


@patch.object(LoadAccountByEmailRepoStub, "load")
def test_should_raise_if_loader_accout_by_email_raise(
    mock_load: MagicMock, sut: DbAuthentication
):
    mock_load.side_effect = Exception("Error on matrix")
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.auth(authentication)
    assert type(excinfo.value) is Exception


@patch.object(LoadAccountByEmailRepoStub, "load")
def test_should_return_none_if_load_account_by_email_returns_none(
    mock_load: MagicMock, sut: DbAuthentication
):
    mock_load.return_value = None
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
