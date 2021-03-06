import pytest
from mock import patch, MagicMock

from app.data import Decrypter, DbLoadAccountByToken


class DecrypterStub(Decrypter):
    def decrypt(self, value: str) -> str:
        return "any_value"


@pytest.fixture
def sut():
    decrypter_stub = DecrypterStub()
    yield DbLoadAccountByToken(decrypter_stub)


@patch.object(DecrypterStub, "decrypt")
def test_should_call_decrypt_with_correct_value(
    mock_decrypt: MagicMock, sut: DbLoadAccountByToken
):
    sut.load_by_token("any_token")
    mock_decrypt.assert_called_with("any_token")
