import mongomock
import pytest

from app.infra import AccountMongoRepo
from app.domain import AddAccountModel


@pytest.fixture
def sut():
    mock_collection = mongomock.MongoClient().db.collection
    sut = AccountMongoRepo(mock_collection)
    yield sut


def test_should_return_an_account(sut: AccountMongoRepo):
    data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )

    account = sut.add(data)
    assert account
    assert account.id
    assert account.name == "valid_name"
    assert account.email == "valid_email@example.com"
    assert account.hashed_password == "valid_password"
