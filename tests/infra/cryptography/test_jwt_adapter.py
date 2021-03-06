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


@patch("app.infra.cryptography.jwt_adapter.jwt.encode")
def test_should_raise_exception_if_encode_raise(
    mock_encode: MagicMock, sut: JwtAdapter
):
    mock_encode.side_effect = Exception()
    with pytest.raises(Exception) as excinfo:
        assert sut.encrypt("any_id")
    assert type(excinfo.value) is Exception


@patch("app.infra.cryptography.jwt_adapter.jwt.decode")
def test_should_call_decode_correct_value(mock_decode: MagicMock, sut: JwtAdapter):
    sut.decrypt("any_token")
    mock_decode.assert_called_with("any_token", "secret")


@patch("app.infra.cryptography.jwt_adapter.jwt.decode")
def test_should_return_a_value_on_decrypt_success(
    mock_decode: MagicMock, sut: JwtAdapter
):
    mock_decode.return_value = "any_value"
    value = sut.decrypt("any_token")
    assert value == "any_value"
