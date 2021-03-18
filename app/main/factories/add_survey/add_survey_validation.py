from app.validations import (
    ValidationComposite,
    RequiredFieldsValidation,
)


def make_add_survey_validation():
    return ValidationComposite(
        [
            RequiredFieldsValidation("question"),
            RequiredFieldsValidation("answers"),
        ]
    )
