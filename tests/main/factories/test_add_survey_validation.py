from app.main import make_add_survey_validation


def test_should_call_validation_composite_with_all_validations():
    validation_composite = make_add_survey_validation()
    expected = [
        "RequiredFieldValidation: question",
        "RequiredFieldValidation: answers",
    ]
    assert len(expected) == len(validation_composite.validations)
    assert not any(
        x != str(y) for x, y in zip(expected, validation_composite.validations)
    )
