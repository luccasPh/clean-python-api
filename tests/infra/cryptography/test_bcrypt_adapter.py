import pytest
from mock import patch, MagicMock

from app.infra import BcryptAdapter

SALT = b"$2b$12$9ITqN6psxZRjP8hN04j8Be"


@pytest.fixture
def sut():
    sut = BcryptAdapter(SALT)
    yield sut


@patch("app.infra.cryptography.bcrypt_adapter.hashpw")
def test_should_call_hash_with_correct_values(
    mock_hashpw: MagicMock, sut: BcryptAdapter
):
    value = "any_value"
    sut.hash(value)
    mock_hashpw.assert_called_with(value.encode("utf-8"), SALT)


@patch("app.infra.cryptography.bcrypt_adapter.hashpw")
def test_should_return_hash_on_hash_success(mock_hashpw: MagicMock, sut: BcryptAdapter):
    value = "hash"
    mock_hashpw.return_value = value.encode("utf-8")
    hash = sut.hash("any_value")
    assert hash == "hash"


@patch("app.infra.cryptography.bcrypt_adapter.hashpw")
def test_should_raise_exception_if_hash_raise(
    mock_hashpw: MagicMock, sut: BcryptAdapter
):
    mock_hashpw.side_effect = Exception()
    with pytest.raises(Exception) as excinfo:
        assert sut.hash("any_value")
    assert type(excinfo.value) is Exception


@patch("app.infra.cryptography.bcrypt_adapter.checkpw")
def test_should_call_compare_with_correct_values(
    mock_checkpw: MagicMock, sut: BcryptAdapter
):
    value = "any_value"
    hash = "any_hash"
    sut.compare(value, hash)
    mock_checkpw.assert_called_with(value.encode("utf-8"), hash.encode("utf-8"))


@patch("app.infra.cryptography.bcrypt_adapter.checkpw")
def test_should_return_true_on_compare_success(
    mock_checkpw: MagicMock, sut: BcryptAdapter
):
    mock_checkpw.return_value = True
    result = sut.compare("any_value", "any_hash")
    assert result


@patch("app.infra.cryptography.bcrypt_adapter.checkpw")
def test_should_return_false_on_compare_fails(
    mock_checkpw: MagicMock, sut: BcryptAdapter
):
    mock_checkpw.return_value = False
    result = sut.compare("any_value", "any_hash")
    assert not result


@patch("app.infra.cryptography.bcrypt_adapter.checkpw")
def test_should_raise_exception_if_compare_raise(
    mock_checkpw: MagicMock, sut: BcryptAdapter
):
    mock_checkpw.side_effect = Exception()
    with pytest.raises(Exception) as excinfo:
        assert sut.compare("any_value", "any_hash")
    assert type(excinfo.value) is Exception
