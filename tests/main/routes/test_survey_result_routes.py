import mongomock
import pytest
from mock import MagicMock, patch
from fastapi.testclient import TestClient
from pymongo.collection import Collection

from app.main.config.app import app

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


@patch("app.main.factories.save_survey_result.get_collection_surveys")
@patch("app.main.factories.save_survey_result.get_collection_survey_results")
@patch("app.main.factories.save_survey_result.get_collection_accounts")
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
    response = client.post(
        "/api/surveys/any_id/results",
        json=dict(answers="any_answer"),
    )
    assert response.status_code == 403
