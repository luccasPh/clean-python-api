import pytest
from mock import patch, MagicMock

from app.domain import AccountModel, AuthenticationModel
from app.data import (
    LoadAccountByEmailRepo,
    DbAuthentication,
    HashComparer,
    TokenGenerator,
    UpdateAccessTokenRepo,
)


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


class TokenGeneratorStub(TokenGenerator):
    def generate(self, id: str) -> str:
        return "access_token"


class UpdateAccessTokenRepoStub(UpdateAccessTokenRepo):
    def update(self, id: str, access_token: str):
        ...


@pytest.fixture
def sut():
    load_account_by_email_repo_stub = LoadAccountByEmailRepoStub()
    hash_comparer_stub = HashComparerStub()
    token_comparer_stub = TokenGeneratorStub()
    update_access_token_repo_stub = UpdateAccessTokenRepoStub()
    return DbAuthentication(
        load_account_by_email_repo_stub,
        hash_comparer_stub,
        token_comparer_stub,
        update_access_token_repo_stub,
    )


@patch.object(LoadAccountByEmailRepoStub, "load")
def test_should_call_loader_accout_by_email_correct_value(
    mock_load_account_by_email_repo_stub: MagicMock, sut: DbAuthentication
):
    sut.auth(AuthenticationModel(email="valid_email@example.com", password="password"))
    mock_load_account_by_email_repo_stub.assert_called_with("valid_email@example.com")


@patch.object(LoadAccountByEmailRepoStub, "load")
def test_should_raise_exception_if_loader_accout_by_email_raise(
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


@patch.object(TokenGeneratorStub, "generate")
def test_should_call_token_generator_correct_value(
    mock_generate: MagicMock, sut: DbAuthentication
):
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    sut.auth(authentication)
    mock_generate.assert_called_with("valid_id")


@patch.object(TokenGeneratorStub, "generate")
def test_should_raise_exception_if_token_generator_raise(
    mock_generate: MagicMock, sut: DbAuthentication
):
    mock_generate.side_effect = Exception("Error on matrix")
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


@patch.object(UpdateAccessTokenRepoStub, "update")
def test_should_call_update_access_token_repo_correct_values(
    mock_update: MagicMock, sut: DbAuthentication
):
    authentication = AuthenticationModel(
        email="valid_email@example.com", password="valid_password"
    )
    sut.auth(authentication)
    mock_update.assert_called_with("valid_id", "access_token")
