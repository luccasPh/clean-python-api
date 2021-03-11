import mongomock
import pytest

from datetime import datetime
from freezegun import freeze_time

from app.infra import SaveSurveyResultMongoRepo
from app.domain import SaveSurveyResultModel, SurveyModel, AccountModel


MOCK_COLLECTION_SURVEYS = mongomock.MongoClient().db.surveys
MOCK_COLLECTION_SURVEY_RESULTS = mongomock.MongoClient().db.survey_results
MOCK_COLLECTION_ACCOUNTS = mongomock.MongoClient().db.accounts


def make_survey() -> SurveyModel:
    MOCK_COLLECTION_SURVEYS.insert_one(
        dict(
            question="any_question",
            answers=[dict(image="any_image", answer="any_answer")],
            date=datetime.utcnow(),
        )
    )
    survey = MOCK_COLLECTION_SURVEYS.find_one()
    survey["id"] = str(survey.pop("_id"))
    return SurveyModel(**survey)


def make_account() -> AccountModel:
    MOCK_COLLECTION_ACCOUNTS.insert_one(
        dict(
            name="any_name",
            email="any_email@example.com",
            hashed_password="any_hashed_password",
        )
    )
    account = MOCK_COLLECTION_ACCOUNTS.find_one()
    account["id"] = str(account.pop("_id"))
    return AccountModel(**account)


@pytest.fixture
def sut():
    yield SaveSurveyResultMongoRepo(
        MOCK_COLLECTION_SURVEYS,
        MOCK_COLLECTION_SURVEY_RESULTS,
        MOCK_COLLECTION_ACCOUNTS,
    )
    MOCK_COLLECTION_SURVEYS.drop()
    MOCK_COLLECTION_SURVEY_RESULTS.drop()
    MOCK_COLLECTION_ACCOUNTS.drop()


@freeze_time("2021-03-09")
def test_should_add_a_survey_result_if_its_new(sut: SaveSurveyResultMongoRepo):
    survey = make_survey()
    account = make_account()
    survey_result = sut.save(
        SaveSurveyResultModel(
            survey_id=survey.id, account_id=account.id, answer=survey.answers[0].answer
        )
    )
    assert survey_result
    assert survey_result.id
    assert survey_result.survey_id == survey.id
    assert survey_result.account_id == account.id
    assert survey_result.answer == survey.answers[0].answer
