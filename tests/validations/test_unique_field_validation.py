import pytest
import mongomock
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


@patch("app.main.decorators.log.get_collection")
@patch.object(DbSearchByFieldStub, "search_by_field")
def test_should_db_search_by_field_raise_exception_if_search_by_field_raise(
    mock_search_by_field: MagicMock,
    mock_get_collection: MagicMock,
    sut: DbSearchByFieldStub,
):
    mock_search_by_field.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    input = {
        "email": "test@example.com",
    }

    with pytest.raises(Exception) as excinfo:
        assert sut.validate(input)
    assert type(excinfo.value) is Exception


@patch.object(DbSearchByFieldStub, "search_by_field")
def test_should_return_unique_value_error_if_db_search_by_field_fails(
    mock_search_by_field: MagicMock, sut: UniqueFieldValidation
):
    mock_search_by_field.return_value = True
    input = {
        "email": "test@example.com",
    }
    result = sut.validate(input)
    assert result.args[0] == "The received email is already in use"
