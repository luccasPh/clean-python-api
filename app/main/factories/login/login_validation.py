from app.utils.email_validator_adapter import EmailValidatorAdapter
from app.presentation import (
    ValidationComposite,
    RequiredFieldValidation,
    EmailValidation,
)


def make_login_validation():
    return ValidationComposite(
        [
            RequiredFieldValidation("email"),
            RequiredFieldValidation("password"),
            EmailValidation(
                "email", EmailValidatorAdapter(check_mx=False, skip_smtp=True)
            ),
        ]
    )
