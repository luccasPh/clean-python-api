import pytest
from mock import patch, MagicMock

from app.validations import ValidationComposite
from app.presentation import Validation


class ValidationStub(Validation):
    def validate(self, input):
        ...


@pytest.fixture
def sut():
    validation_stub = ValidationStub()
    sut = ValidationComposite([validation_stub, validation_stub, validation_stub])
    yield sut


@patch.object(ValidationStub, "validate")
def test_should_return_an_error_if_any_validation_fails(
    mock_validate: MagicMock,
    sut: ValidationComposite,
):
    mock_validate.return_value = Exception("field error")
    input = dict(field="field")
    is_error = sut.validate(input)
    assert is_error.args[0] == "field error"


@patch.object(ValidationStub, "validate")
def test_should_return_the_first_error_if_many_validation_fails(
    mock_validate: MagicMock,
    sut: ValidationComposite,
):
    mock_validate.side_effect = [
        Exception("first error"),
        Exception("second error"),
        Exception("third error"),
    ]
    input = dict(field="field")

    with pytest.raises(Exception) as excinfo:
        sut.validate(input)

    assert excinfo.value.args[0] == "first error"


def test_should_not_return_if_all_validation_succeeds(
    sut: ValidationComposite,
):
    input = dict(field="field")
    is_error = sut.validate(input)
    assert not is_error
