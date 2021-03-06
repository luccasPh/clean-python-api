from app.validations import (
    ValidationComposite,
    RequiredFieldValidation,
)


def make_add_survey_validation():
    return ValidationComposite(
        [
            RequiredFieldValidation("question"),
            RequiredFieldValidation("answers"),
        ]
    )
