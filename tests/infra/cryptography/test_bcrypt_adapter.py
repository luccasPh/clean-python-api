import pytest
from mock import patch, MagicMock

from app.infra import BcryptAdapter

SALT = 12


@pytest.fixture
def sut():
    sut = BcryptAdapter(SALT)
    yield sut


@patch("app.infra.cryptography.bcrypt_adapter.hashpw")
def test_should_call_bcrypt_with_correct_values(
    mock_hashpw: MagicMock, sut: BcryptAdapter
):
    sut.encrypt("any_value")
    mock_hashpw.assert_called_with("any_value", SALT)
