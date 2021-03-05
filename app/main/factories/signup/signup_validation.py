from app.infra import EmailValidatorAdapter
from app.infra import MongoDbAdapter, get_collection
from app.validations import (
    ValidationComposite,
    RequiredFieldValidation,
    CompareFieldsValidation,
    EmailValidation,
    UniqueFieldValidation,
)


def make_signup_validation():
    return ValidationComposite(
        [
            RequiredFieldValidation("name"),
            RequiredFieldValidation("email"),
            RequiredFieldValidation("password"),
            RequiredFieldValidation("password_confirmation"),
            CompareFieldsValidation("password", "password_confirmation"),
            EmailValidation(
                "email", EmailValidatorAdapter(check_mx=False, skip_smtp=True)
            ),
            UniqueFieldValidation("email", MongoDbAdapter(get_collection("accounts"))),
        ]
    )
