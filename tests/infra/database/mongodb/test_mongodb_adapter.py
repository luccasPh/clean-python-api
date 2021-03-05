import pytest
import mongomock
from mock import patch, MagicMock

from app.infra import MongoDbAdapter

MOCK_COLLECTION = mongomock.MongoClient().db.collection


@pytest.fixture
def sut():
    yield MongoDbAdapter(MOCK_COLLECTION)
    MOCK_COLLECTION.drop()


@patch.object(MOCK_COLLECTION, "find")
def test_should_calls_collection_find_correct_values(
    mock_find: MagicMock, sut: MongoDbAdapter
):
    sut.search_by_field("email", "test@example.com")
    mock_find.assert_called_with({"email": "test@example.com"})


@patch.object(MOCK_COLLECTION, "find")
def test_should_raise_exception_if_collection_find_raise(
    mock_find: MagicMock, sut: MongoDbAdapter
):
    mock_find.side_effect = Exception()
    with pytest.raises(Exception) as excinfo:
        assert sut.search_by_field("email", "test@example.com")
    assert type(excinfo.value) is Exception
