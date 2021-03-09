import mongomock
import pytest
import jwt
from mock import MagicMock, patch
from fastapi.testclient import TestClient
from pymongo.collection import Collection

from app.main.config.app import app
from app.main.config import env

client = TestClient(app)


@pytest.fixture
def mock_collection():
    mock = mongomock.MongoClient().db.collection
    yield mock
    mock.drop()


@patch("app.main.factories.survey.add_survey_factory.get_collection")
def test_should_403_on_add_surveys_without_token(
    mock_factory_get_collection: MagicMock,
    mock_collection: Collection,
):
    mock_factory_get_collection.return_value = mock_collection
    response = client.post(
        "/api/surveys",
        json=dict(
            question="Question 1",
            answers=[
                dict(answer="Answer 1", image="http://any_image"),
                dict(answer="Answer 2"),
            ],
        ),
    )
    assert response.status_code == 403


@patch("app.main.factories.survey.add_survey_factory.get_collection")
@patch("app.main.factories.middlewares.aut_middleware_factory.get_collection")
def test_should_204_on_add_surveys_wit_valid_token(
    mock_factory_survey_get_collection: MagicMock,
    mock_factory_middleware_get_collection: MagicMock,
    mock_collection: Collection,
):
    mock_factory_survey_get_collection.return_value = mock_collection
    mock_factory_middleware_get_collection.return_value = mock_collection
    account_id = mock_collection.insert_one(
        dict(
            name="John", email="email@example.com", hashed_password="123", role="admin"
        )
    ).inserted_id
    access_token = jwt.encode({"id": str(account_id)}, env.JWT_SECRET_KEY)
    mock_collection.update_one(
        {"_id": account_id}, {"$set": {"access_token": access_token}}
    )

    response = client.post(
        "/api/surveys",
        headers={"x-access-token": access_token},
        json=dict(
            question="Question 1",
            answers=[
                dict(answer="Answer 1", image="http://any_image"),
                dict(answer="Answer 2"),
            ],
        ),
    )
    assert response.status_code == 204
