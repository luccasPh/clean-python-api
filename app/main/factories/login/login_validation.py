from app.infra import EmailValidatorAdapter
from app.validations import (
    ValidationComposite,
    RequiredFieldsValidation,
    EmailValidation,
)


def make_login_validation():
    return ValidationComposite(
        [
            RequiredFieldsValidation("email"),
            RequiredFieldsValidation("password"),
            EmailValidation(
                "email",
                EmailValidatorAdapter(check_mx=False, skip_smtp=True),
            ),
        ]
    )
