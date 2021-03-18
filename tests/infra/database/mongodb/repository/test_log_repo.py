import mongomock
import pytest

from app.infra import LogMongoRepo


@pytest.fixture
def sut():
    mock_collection = mongomock.MongoClient().db.collection
    sut = LogMongoRepo(mock_collection)
    yield (sut, mock_collection)


def test_should_return_an_log(sut):
    traceback = "Error on matrix"
    sut[0].log(traceback)
    log = sut[1].find_one()
    assert log
    assert log["traceback"] == "Error on matrix"
    assert log["date"]
