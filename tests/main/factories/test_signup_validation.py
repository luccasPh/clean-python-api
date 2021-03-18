from app.main import make_signup_validation


def test_should_call_validation_composite_with_all_validations():
    validation_composite = make_signup_validation()
    expected = [
        "RequiredFieldValidation: signup",
        "CompareFieldsValidation: password -> password_confirmation",
        "EmailValidation: email",
        "UniqueFieldValidation: email",
    ]
    assert len(expected) == len(validation_composite.validations)
    assert not any(
        x != str(y) for x, y in zip(expected, validation_composite.validations)
    )
