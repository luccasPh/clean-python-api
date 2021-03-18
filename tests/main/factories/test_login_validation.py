from app.main import make_login_validation


def test_should_call_validation_composite_with_all_validations():
    validation_composite = make_login_validation()
    expected = [
        "RequiredFieldValidation: login",
        "EmailValidation: email",
    ]
    assert len(expected) == len(validation_composite.validations)
    assert not any(
        x != str(y) for x, y in zip(expected, validation_composite.validations)
    )
