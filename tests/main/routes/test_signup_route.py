import mongomock
from mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main.config.app import app

client = TestClient(app)


@patch("app.main.factories.signup.signup_factory.get_collection")
def test_should_return_an_account(test_get_collection: MagicMock):
    test_get_collection.return_value = mongomock.MongoClient().db.collection
    response = client.post(
        "/api/signup",
        json=dict(
            name="John",
            email="foo@example.com",
            password="123",
            password_confirmation="123",
        ),
    )
    expected_response = response.json()
    assert response.status_code == 200
    assert expected_response["id"]
    assert expected_response["name"] == "John"
    assert expected_response["email"] == "foo@example.com"
