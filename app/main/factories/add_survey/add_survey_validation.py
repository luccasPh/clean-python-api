from schema import Schema, And

from app.validations import (
    ValidationComposite,
    RequiredFieldsValidation,
)


def make_add_survey_validation():
    add_survey_schema = Schema(
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
            RequiredFieldsValidation(add_survey_schema, "add_survey"),
        ]
    )
