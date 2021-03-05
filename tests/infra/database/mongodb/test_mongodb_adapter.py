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
def test_should_calls_collection_find_correct_value(
    mock_find: MagicMock, sut: MongoDbAdapter
):
    sut.search_by_field("email", "test@example.com")
    mock_find.assert_called_with({"email": "test@example.com"})
