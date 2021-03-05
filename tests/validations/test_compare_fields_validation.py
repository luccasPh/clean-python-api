import pytest

from app.validations import CompareFieldsValidation


@pytest.fixture
def sut():
    sut = CompareFieldsValidation("field_1", "field_2")
    yield sut


def test_should_return_invalid_param_error_if_validation_fails(
    sut: CompareFieldsValidation,
):
    input = dict(field_1="value", field_2="wrong_value")
    is_error = sut.validate(input)
    assert is_error.args[0] == "Invalid param: field_2"


def test_should_not_return_if_validation_succeeds(
    sut: CompareFieldsValidation,
):
    input = dict(field_1="value", field_2="value")
    is_error = sut.validate(input)
    assert not is_error
