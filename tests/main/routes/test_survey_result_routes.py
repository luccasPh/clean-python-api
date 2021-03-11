import mongomock
import pytest
import jwt
from mock import MagicMock, patch
from fastapi.testclient import TestClient
from pymongo.collection import Collection
from datetime import datetime

from app.main.config.app import app
from app.main.config import env

client = TestClient(app)


@pytest.fixture
def mock_collection_accounts():
    mock = mongomock.MongoClient().db.accounts
    yield mock
    mock.drop()


@pytest.fixture
def mock_collection_surveys():
    mock = mongomock.MongoClient().db.surveys
    yield mock
    mock.drop()


@pytest.fixture
def mock_collection_survey_results():
    mock = mongomock.MongoClient().db.survey_results
    yield mock
    mock.drop()


@patch(
    "app.main.factories.save_survey_result.save_survey_result_factory.get_collection_surveys"
)
@patch(
    "app.main.factories.save_survey_result.save_survey_result_factory.get_collection_survey_results"  # flake8: noqa
)
@patch(
    "app.main.factories.save_survey_result.save_survey_result_factory.get_collection_accounts"
)
def test_should_403_on_save_survey_result_without_token(
    mock_get_collection_accounts: MagicMock,
    mock_get_collection_survey_results: MagicMock,
    mock_get_collection_surveys: MagicMock,
    mock_collection_survey_results: Collection,
    mock_collection_surveys: Collection,
    mock_collection_accounts: Collection,
):
    mock_get_collection_accounts.return_value = mock_collection_accounts
    mock_get_collection_surveys.return_value = mock_collection_surveys
    mock_get_collection_survey_results.return_value = mock_collection_survey_results
    response = client.put(
        "/api/surveys/any_id/results",
        json=dict(answers="any_answer"),
    )
    assert response.status_code == 403


@patch("app.main.factories.middlewares.aut_middleware_factory.get_collection")
@patch(
    "app.main.factories.save_survey_result.save_survey_result_factory.get_collection_surveys"
)
@patch(
    "app.main.factories.save_survey_result.save_survey_result_factory.get_collection_survey_results"  # flake8: noqa
)
@patch(
    "app.main.factories.save_survey_result.save_survey_result_factory.get_collection_accounts"
)
def test_should_200_on_load_surveys_wit_valid_token(
    mock_get_collection_accounts: MagicMock,
    mock_get_collection_survey_results: MagicMock,
    mock_get_collection_surveys: MagicMock,
    mock_factory_middleware_get_collection: MagicMock,
    mock_collection_survey_results: Collection,
    mock_collection_surveys: Collection,
    mock_collection_accounts: Collection,
):
    mock_get_collection_accounts.return_value = mock_collection_accounts
    mock_get_collection_surveys.return_value = mock_collection_surveys
    mock_get_collection_survey_results.return_value = mock_collection_survey_results
    mock_factory_middleware_get_collection.return_value = mock_collection_accounts
    account_id = mock_collection_accounts.insert_one(
        dict(
            name="John", email="email@example.com", hashed_password="123", role="admin"
        )
    ).inserted_id
    access_token = jwt.encode({"id": str(account_id)}, env.JWT_SECRET_KEY)
    mock_collection_accounts.update_one(
        {"_id": account_id}, {"$set": {"access_token": access_token}}
    )
    survey_id = mock_collection_surveys.insert_one(
        dict(
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
            date=datetime.utcnow(),
        )
    ).inserted_id
    response = client.put(
        f"/api/surveys/{str(survey_id)}/results",
        headers={"x-access-token": access_token},
        json=dict(answer="any_answer"),
    )
    assert response.status_code == 200
