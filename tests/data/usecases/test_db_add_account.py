import pytest
from mock import MagicMock, patch

from app.data import DbAddAccount
from app.domain import AddAccountModel


class EncrypterStub:
    def encrypt(self, value: str) -> str:
        return "hashed_password"


@pytest.fixture
def sut():
    encrypterStub = EncrypterStub()
    sut = DbAddAccount(encrypterStub)
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
