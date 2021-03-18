from schema import Schema, And

from app.infra import EmailValidatorAdapter
from app.validations import (
    ValidationComposite,
    RequiredFieldsValidation,
    EmailValidation,
)


def make_login_validation():
    login_schema = Schema(
        dict(
            email=And(str, len, error="Invalid key: 'email'"),
            password=And(str, len, error="Invalid key: 'password'"),
        )
    )
    return ValidationComposite(
        [
            RequiredFieldsValidation(login_schema, "login"),
            EmailValidation(
                "email",
                EmailValidatorAdapter(check_mx=False, skip_smtp=True),
            ),
        ]
    )
