import pytest

from app.utils.email_validator_adapter import EmailValidatorAdapter
from app.presentation import EmailValidator


@pytest.fixture
def sut():
    sut = EmailValidatorAdapter()
    yield sut


def test_should_return_false_if_validator_is_false(sut: EmailValidator):
    is_valid = sut.is_valid("invalid_email@example.com")
    assert not is_valid
