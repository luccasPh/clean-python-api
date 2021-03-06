import pytest
from mock import patch, MagicMock

from app.infra import EmailValidatorAdapter
from app.validations import EmailValidator

CHECK_MX = False
SKIP_SMTP = True


@pytest.fixture
def sut():
    sut = EmailValidatorAdapter(CHECK_MX, SKIP_SMTP)
    yield sut


@patch("app.infra.validators.email_validator_adapter.validate_email")
def test_should_return_false_if_validator_is_false(
    mock_validate_email: MagicMock, sut: EmailValidator
):
    mock_validate_email.return_value = False
    is_valid = sut.is_valid("invalid_email@example.com")
    assert not is_valid


def test_should_return_true_if_validator_is_true(sut: EmailValidator):
    is_valid = sut.is_valid("valid_email@example.com")
    assert is_valid


@patch("app.infra.validators.email_validator_adapter.validate_email")
def test_should_call_validator_with_correct_email(
    mock_validate_email: MagicMock, sut: EmailValidator
):
    sut.is_valid("valid_email@example.com")
    mock_validate_email.assert_called_once_with(
        "valid_email@example.com", check_mx=CHECK_MX, skip_smtp=SKIP_SMTP
    )
