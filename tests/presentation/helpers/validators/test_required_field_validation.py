import pytest

from app.presentation import RequiredFieldValidation


@pytest.fixture
def sut():
    sut = RequiredFieldValidation("any_field")
    yield sut


def test_should_return_missing_param_error_if_validation_fails(
    sut: RequiredFieldValidation,
):
    input = dict(field="other_field")
    is_error = sut.validate(input)
    assert is_error.args[0] == "Missing param: any_field"
