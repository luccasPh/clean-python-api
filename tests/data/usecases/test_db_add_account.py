import pytest
from mock import patch

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
def test_should_call_encrypter_with_correct_value(test_encrypt, sut: DbAddAccount):
    account_data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )
    sut.add(account_data)
    test_encrypt.assert_called_with("valid_password")
