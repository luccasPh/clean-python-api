import pytest
from mock import patch, MagicMock

from app.infra import JwtAdapter


@pytest.fixture
def sut():
    return JwtAdapter("secret")


@patch("app.infra.cryptography.jwt_adapter.jwt.encode")
def test_should_call_encode_correct_value(mock_encode: MagicMock, sut: JwtAdapter):
    sut.encrypt("any_id")
    mock_encode.assert_called_with(dict(id="any_id"), "secret")


@patch("app.infra.cryptography.jwt_adapter.jwt.encode")
def test_should_return_an_access_token_on_success(
    mock_encode: MagicMock, sut: JwtAdapter
):
    mock_encode.return_value = "any_token"
    accesse_token = sut.encrypt("any_id")
    assert accesse_token == "any_token"
