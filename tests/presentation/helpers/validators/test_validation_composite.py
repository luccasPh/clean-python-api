import pytest
from mock import patch, MagicMock

from app.presentation import ValidationComposite, Validation


class ValidationStub(Validation):
    def validate(self, input):
        ...


@pytest.fixture
def sut():
    validation_stub = ValidationStub()
    sut = ValidationComposite([validation_stub])
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
