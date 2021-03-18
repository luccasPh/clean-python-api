from schema import Schema, And, Optional

from app.validations import (
    ValidationComposite,
    RequiredFieldsValidation,
)


def make_add_survey_validation():
    add_survey_schema = Schema(
        dict(
            question=And(str, len, error="Invalid key: 'question'"),
            answers=And(
                And(list, len, error="Invalid key: 'answers'"),
                Schema(
                    [
                        {
                            Optional("image"): And(
                                str, len, error="Invalid key: 'image'"
                            ),
                            "answer": And(str, len, error="Invalid key: 'answer'"),
                        },
                    ],
                    error="Missing key: 'answer'",
                ),
            ),
        )
    )
    return ValidationComposite(
        [
            RequiredFieldsValidation(add_survey_schema, "add_survey"),
        ]
    )
