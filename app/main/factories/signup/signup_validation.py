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
    return ValidationComposite(
        [
            RequiredFieldsValidation("name"),
            RequiredFieldsValidation("email"),
            RequiredFieldsValidation("password"),
            RequiredFieldsValidation("password_confirmation"),
            CompareFieldsValidation("password", "password_confirmation"),
            EmailValidation(
                "email", EmailValidatorAdapter(check_mx=False, skip_smtp=True)
            ),
            UniqueFieldValidation("email", MongoDbAdapter(get_collection("accounts"))),
        ]
    )
