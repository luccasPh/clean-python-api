from schema import Schema, And

from app.infra import EmailValidatorAdapter
from app.infra import MongoDbAdapter, get_collection
from app.validations import (
    ValidationComposite,
    RequiredFieldsValidation,
    CompareFieldsValidation,
    EmailValidation,
    UniqueFieldValidation,
)


def make_signup_validation():
    signup_schema = Schema(
        dict(
            name=And(str, len, error="Invalid key: 'name'"),
            email=And(str, len, error="Invalid key: 'email'"),
            password=And(
                And(str, len, error="Invalid key: 'password'"),
                And(
                    lambda s: len(s) > 5,
                    error="Invalid key: 'password minimum 6 characters'",
                ),
            ),
            password_confirmation=And(
                And(str, len, error="Invalid key: 'password_confirmation'"),
            ),
        )
    )
    return ValidationComposite(
        [
            RequiredFieldsValidation(signup_schema, "signup"),
            CompareFieldsValidation("password", "password_confirmation"),
            EmailValidation(
                "email", EmailValidatorAdapter(check_mx=False, skip_smtp=True)
            ),
            UniqueFieldValidation("email", MongoDbAdapter(get_collection("accounts"))),
        ]
    )
