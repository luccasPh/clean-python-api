import pytest
from mock import patch, MagicMock

from app.infra import BcryptAdapter

SALT = b"$2b$12$9ITqN6psxZRjP8hN04j8Be"


@pytest.fixture
def sut():
    sut = BcryptAdapter(SALT)
    yield sut


@patch("app.infra.cryptography.bcrypt_adapter.hashpw")
def test_should_call_bcrypt_with_correct_values(
    mock_hashpw: MagicMock, sut: BcryptAdapter
):
    value = "any_value"
    sut.encrypt(value)
    mock_hashpw.assert_called_with(value.encode("utf-8"), SALT)


@patch("app.infra.cryptography.bcrypt_adapter.hashpw")
def test_should_return_hash(mock_hashpw: MagicMock, sut: BcryptAdapter):
    value = "hash"
    mock_hashpw.return_value = value.encode("utf-8")
    hash = sut.encrypt("any_value")
    assert hash == "hash"


@patch("app.infra.cryptography.bcrypt_adapter.hashpw")
def test_should_raise_if_bcrypt_raise(mock_hashpw: MagicMock, sut: BcryptAdapter):
    mock_hashpw.side_effect = Exception()
    with pytest.raises(Exception) as excinfo:
        assert sut.encrypt("any_value")
    assert type(excinfo.value) is Exception
