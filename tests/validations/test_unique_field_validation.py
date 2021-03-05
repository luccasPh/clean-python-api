import pytest
from mock import patch, MagicMock

from app.validations import UniqueFieldValidation, DbSearchByField


class DbSearchByFieldStub(DbSearchByField):
    def search_by_field(self, field: str, value: str) -> bool:
        return False


@pytest.fixture
def sut():
    db_search_by_field_stub = DbSearchByFieldStub()
    sut = UniqueFieldValidation("email", db_search_by_field_stub)
    yield sut


@patch.object(DbSearchByFieldStub, "search_by_field")
def test_should_db_search_by_field_calls_search_by_field_correct_value(
    mock_search_by_field: MagicMock, sut: UniqueFieldValidation
):
    input = {
        "email": "test@example.com",
    }
    sut.validate(input)
    mock_search_by_field.assert_called_with("email", "test@example.com")
