from app.infra import EmailValidatorAdapter
from app.infra import AccountMongoRepo, get_collection
from app.validations import (
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
                "email",
                EmailValidatorAdapter(check_mx=False, skip_smtp=True),
                AccountMongoRepo(get_collection("accounts")),
            ),
        ]
    )
