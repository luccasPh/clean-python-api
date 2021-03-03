import mongomock
import pytest

from app.infra import AccountMongoRepo
from app.domain import AddAccountModel


MOCK_COLLECTION = mongomock.MongoClient().db.collection


@pytest.fixture
def sut():
    yield AccountMongoRepo(MOCK_COLLECTION)
    MOCK_COLLECTION.drop()


def test_should_return_an_account_on_add_success(sut: AccountMongoRepo):
    data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )

    account = sut.add(data)
    assert account
    assert account.id
    assert account.name == "valid_name"
    assert account.email == "valid_email@example.com"
    assert account.hashed_password == "valid_password"


def test_should_return_an_account_on_load_by_email_success(sut: AccountMongoRepo):
    MOCK_COLLECTION.insert_one(
        dict(
            name="valid_name",
            email="valid_email@example.com",
            hashed_password="hashed_password",
        )
    )

    account = sut.load_by_email("valid_email@example.com")
    assert account
    assert account.id
    assert account.name == "valid_name"
    assert account.email == "valid_email@example.com"
    assert account.hashed_password == "hashed_password"


def test_should_return_none_if_load_by_email_fails(sut: AccountMongoRepo):
    account = sut.load_by_email("valid_email@example.com")
    assert not account


def test_update_the_account_access_token_on_update_idem_on_success(
    sut: AccountMongoRepo,
):
    account_id = MOCK_COLLECTION.insert_one(
        dict(
            name="valid_name",
            email="valid_email@example.com",
            hashed_password="hashed_password",
        )
    ).inserted_id

    sut.update_access_token(account_id, "any_token")
    account = MOCK_COLLECTION.find_one({"_id": account_id})
    assert account
    assert account["access_token"] == "any_token"
