from app.presentation import (
    ValidationComposite,
    RequiredFieldValidation,
    CompareFieldsValidation,
)


def make_signup_validation():
    return ValidationComposite(
        [
            RequiredFieldValidation("name"),
            RequiredFieldValidation("email"),
            RequiredFieldValidation("password"),
            RequiredFieldValidation("password_confirmation"),
            CompareFieldsValidation("password", "password_confirmation"),
        ]
    )
