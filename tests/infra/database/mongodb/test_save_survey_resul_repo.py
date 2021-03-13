import mongomock
import pytest
from datetime import datetime
from freezegun import freeze_time
from bson.objectid import ObjectId

from app.infra import SaveSurveyResultMongoRepo
from app.domain import SaveSurveyResultModel, SurveyModel, AccountModel


MOCK_DATABASE = mongomock.MongoClient().db


def make_survey() -> SurveyModel:
    MOCK_DATABASE["surveys"].insert_one(
        dict(
            question="any_question",
            answers=[
                dict(image="any_image", answer="any_answer"),
                dict(image="other_image", answer="other_answer"),
            ],
            date=datetime.utcnow(),
        )
    )
    survey = MOCK_DATABASE["surveys"].find_one()
    survey["id"] = str(survey.pop("_id"))
    return SurveyModel(**survey)


def make_account() -> AccountModel:
    MOCK_DATABASE["accounts"].insert_one(
        dict(
            name="any_name",
            email="any_email@example.com",
            hashed_password="any_hashed_password",
        )
    )
    account = MOCK_DATABASE["accounts"].find_one()
    account["id"] = str(account.pop("_id"))
    return AccountModel(**account)


@pytest.fixture
def sut():
    yield SaveSurveyResultMongoRepo(
        MOCK_DATABASE["surveys"],
        MOCK_DATABASE["survey_results"],
    )
    MOCK_DATABASE["accounts"].drop()
    MOCK_DATABASE["surveys"].drop()
    MOCK_DATABASE["survey_results"].drop()


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
    assert survey_result.survey_id == survey.id
    assert survey_result.answers[0].answer == survey.answers[0].answer
    assert survey_result.answers[0].count == 1
    assert survey_result.answers[0].percent == 100


@freeze_time("2021-03-09")
def test_should_update_a_survey_result_if_its_not_new(sut: SaveSurveyResultMongoRepo):
    survey = make_survey()
    account = make_account()
    MOCK_DATABASE["survey_results"].insert_one(
        dict(
            survey_id=ObjectId(survey.id),
            account_id=ObjectId(account.id),
            answer=survey.answers[0].answer,
            date=datetime.utcnow(),
        )
    )
    survey_result = sut.save(
        SaveSurveyResultModel(
            survey_id=survey.id, account_id=account.id, answer=survey.answers[1].answer
        )
    )
    assert survey_result
    assert survey_result.survey_id == survey.id
    assert survey_result.answers[0].answer == survey.answers[1].answer
    assert survey_result.answers[0].count == 1
    assert survey_result.answers[0].percent == 100
