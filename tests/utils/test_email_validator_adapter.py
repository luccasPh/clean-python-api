import pytest
import mock

from app.utils.email_validator_adapter import EmailValidatorAdapter
from app.presentation import EmailValidator


@pytest.fixture
def sut():
    sut = EmailValidatorAdapter()
    yield sut


@mock.patch("app.utils.email_validator_adapter.validate_email")
def test_should_return_false_if_validator_is_false(
    test_validate_email, sut: EmailValidator
):
    test_validate_email.return_value = False
    is_valid = sut.is_valid("invalid_email@example.com")
    assert not is_valid


def test_should_return_true_if_validator_is_true(sut: EmailValidator):
    is_valid = sut.is_valid("valid_email@example.com")
    assert is_valid


@mock.patch("app.utils.email_validator_adapter.validate_email")
def test_should_call_validator_with_correct_email(
    test_validate_email, sut: EmailValidator
):
    sut.is_valid("valid_email@example.com")
    test_validate_email.assert_called_with("valid_email@example.com")
