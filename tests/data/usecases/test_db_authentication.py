import pytest
from mock import patch, MagicMock

from app.domain import AccountModel, AuthenticationModel
from app.data import LoadAccountByEmailRepo, DbAuthentication


class LoadAccountByEmailRepoStub(LoadAccountByEmailRepo):
    def load(self, email: str) -> AccountModel:
        account = AccountModel(
            id="valid_id",
            name="valid_name",
            email="valid_email",
            hashed_password="valid_hashed_password",
        )
        return account


@pytest.fixture
def sut():
    load_account_by_email_repo_stub = LoadAccountByEmailRepoStub()
    return DbAuthentication(load_account_by_email_repo_stub)


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
