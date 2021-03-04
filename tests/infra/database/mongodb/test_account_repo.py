import mongomock
import pytest
from mock import patch, MagicMock

from app.infra import AccountMongoRepo
from app.domain import AddAccountModel


MOCK_COLLECTION = mongomock.MongoClient().db.collection


@pytest.fixture
def sut():
    yield AccountMongoRepo(MOCK_COLLECTION)
    MOCK_COLLECTION.drop()


@patch.object(MOCK_COLLECTION, "insert_one")
def test_should_call_collection_insert_with_correct_values_on_add(
    mock_insert_one: MagicMock, sut: AccountMongoRepo
):
    data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )

    sut.add(data)
    mock_insert_one.assert_called_with(
        dict(
            name="valid_name",
            email="valid_email@example.com",
            hashed_password="valid_password",
        )
    )


def test_should_create_an_account_on_add(sut: AccountMongoRepo):
    data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )

    sut.add(data)
    expected = MOCK_COLLECTION.find_one()
    assert expected
    assert expected["_id"]
    assert expected["name"] == "valid_name"
    assert expected["email"] == "valid_email@example.com"
    assert expected["hashed_password"] == "valid_password"


@patch.object(MOCK_COLLECTION, "insert_one")
def test_should_raise_exception_if_collection_insert_raise_on_add(
    mock_insert_one: MagicMock, sut: AccountMongoRepo
):
    mock_insert_one.side_effect = Exception()
    data = AddAccountModel(
        name="valid_name", email="valid_email@example.com", password="valid_password"
    )
    with pytest.raises(Exception) as excinfo:
        assert sut.add(data)
    assert type(excinfo.value) is Exception


@patch.object(MOCK_COLLECTION, "find_one")
def test_should_call_collection_find_with_correct_value_on_load_by_email(
    find_one: MagicMock, sut: AccountMongoRepo
):
    sut.load_by_email("valid_email@example.com")
    find_one.assert_called_with({"email": "valid_email@example.com"})


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


@patch.object(MOCK_COLLECTION, "find_one")
def test_should_raise_exception_if_collection_find_raise_on_load_by_email(
    mock_find_one: MagicMock, sut: AccountMongoRepo
):
    mock_find_one.side_effect = Exception()
    with pytest.raises(Exception) as excinfo:
        assert sut.load_by_email("valid_email@example.com")
    assert type(excinfo.value) is Exception


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
