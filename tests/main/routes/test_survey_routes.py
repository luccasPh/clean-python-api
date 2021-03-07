import mongomock
import pytest
from mock import MagicMock, patch
from fastapi.testclient import TestClient
from pymongo.collection import Collection

from app.main.config.app import app

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
