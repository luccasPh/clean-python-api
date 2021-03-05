from app.utils.email_validator_adapter import EmailValidatorAdapter
from app.infra import AccountMongoRepo, get_collection
from app.presentation import (
    ValidationComposite,
    RequiredFieldValidation,
    CompareFieldsValidation,
    EmailValidation,
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
                "email",
                EmailValidatorAdapter(check_mx=False, skip_smtp=True),
                AccountMongoRepo(get_collection("accounts")),
            ),
        ]
    )
