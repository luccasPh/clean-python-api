from app.presentation import ValidationComposite, RequiredFieldValidation


def make_signup_validation():
    return ValidationComposite(
        [
            RequiredFieldValidation("name"),
            RequiredFieldValidation("email"),
            RequiredFieldValidation("password"),
            RequiredFieldValidation("password_confirmation"),
        ]
    )
