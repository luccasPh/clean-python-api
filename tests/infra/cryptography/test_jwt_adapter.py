import pytest
from mock import patch, MagicMock
from datetime import datetime, timedelta

from app.main.config import env
from app.infra import JwtAdapter

EXPIRATION_TIME = datetime.utcnow() + timedelta(hours=env.JWT_EXPIRATION_TIME)


@pytest.fixture
def sut():
    return JwtAdapter(
        secret="secret", expiration_time=EXPIRATION_TIME, algorithm="HS256"
    )


@patch("app.infra.cryptography.jwt_adapter.jwt.encode")
def test_should_call_encode_correct_value(mock_encode: MagicMock, sut: JwtAdapter):
    sut.encrypt("any_id")
    mock_encode.assert_called_with(
        {"id": "any_id", "exp": EXPIRATION_TIME}, "secret", algorithm="HS256"
    )


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
    mock_decode.assert_called_with("any_token", "secret", algorithms=["HS256"])


@patch("app.infra.cryptography.jwt_adapter.jwt.decode")
def test_should_return_a_value_on_decrypt_success(
    mock_decode: MagicMock, sut: JwtAdapter
):
    mock_decode.return_value = {"id": "any_id"}
    value = sut.decrypt("any_token")
    assert value == "any_id"


@patch("app.infra.cryptography.jwt_adapter.jwt.decode")
def test_should_raise_exception_if_decode_raise(
    mock_decode: MagicMock, sut: JwtAdapter
):
    mock_decode.side_effect = Exception()
    with pytest.raises(Exception) as excinfo:
        assert sut.decrypt("any_id")
    assert type(excinfo.value) is Exception
