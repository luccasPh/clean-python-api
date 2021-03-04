import mongomock
import pytest
from mock import MagicMock, patch
from fastapi.testclient import TestClient
from pymongo.collection import Collection
from bcrypt import hashpw

from app.main.config.app import app

client = TestClient(app)


@pytest.fixture
def mock_collection():
    mock = mongomock.MongoClient().db.collection
    yield mock
    mock.drop()


@patch("app.main.factories.signup.signup_factory.get_collection")
def test_should_204_on_signup(
    mock_get_collection: MagicMock, mock_collection: Collection
):
    mock_get_collection.return_value = mock_collection
    response = client.post(
        "/api/signup",
        json=dict(
            name="John",
            email="foo@example.com",
            password="123",
            password_confirmation="123",
        ),
    )
    assert response.status_code == 204


@patch("app.main.factories.login.login_factory.get_collection")
def test_should_200_on_login(
    mock_get_collection: MagicMock, mock_collection: Collection
):
    mock_get_collection.return_value = mock_collection
    value = "123"
    hashed_password = hashpw(
        value.encode("utf-8"), salt=b"$2b$12$9ITqN6psxZRjP8hN04j8Be"
    ).decode("utf-8")
    mock_collection.insert_one(
        dict(name="John", email="email@example.com", hashed_password=hashed_password)
    )
    response = client.post(
        "/api/login",
        json=dict(email="email@example.com", password="123"),
    )

    assert response.status_code == 200


@patch("app.main.factories.login.login_factory.get_collection")
def test_should_401_on_login(
    mock_get_collection: MagicMock, mock_collection: Collection
):
    mock_get_collection.return_value = mock_collection
    response = client.post(
        "/api/login",
        json=dict(email="email@example.com", password="123"),
    )

    assert response.status_code == 401
