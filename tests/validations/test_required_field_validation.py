import pytest
from schema import Schema, And
from mock import patch, MagicMock

from app.validations import RequiredFieldValidation


@pytest.fixture
def sut():
    schema = Schema(dict(field=And(str, len, error="Invalid key: 'field'")))
    sut = RequiredFieldValidation(schema)
    yield sut


@patch("app.validations.validators.required_field_validation.Schema.validate")
def test_should_calls_schema_validation_with_values(
    mock_validate: MagicMock, sut: RequiredFieldValidation
):
    input = dict(field="any_field")
    sut.validate(input)
    mock_validate.assert_called_with({"field": "any_field"})


def test_should_return_missing_param_error_if_validation_fails(
    sut: RequiredFieldValidation,
):
    input = dict()
    is_error = sut.validate(input)
    assert is_error.args[0] == "Missing param: 'field'"


def test_should_not_return_if_validation_succeeds(
    sut: RequiredFieldValidation,
):
    input = dict(field="any_field")
    is_error = sut.validate(input)
    assert not is_error
