import mongomock
import pytest
from mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time

from app.infra import SurveyMongoRepo
from app.domain import AddSurveyModel


MOCK_COLLECTION = mongomock.MongoClient().db.collection


@pytest.fixture
def sut():
    yield SurveyMongoRepo(MOCK_COLLECTION)
    MOCK_COLLECTION.drop()


@freeze_time("2021-03-09")
@patch.object(MOCK_COLLECTION, "insert_one")
def test_should_call_insert_with_correct_values_on_add(
    mock_insert_one: MagicMock, sut: SurveyMongoRepo
):
    survey_data = dict(
        question="any_question",
        answers=[
            dict(answer="any_answer", image="any_image"),
            dict(answer="other_answer", image=None),
        ],
    )
    sut.add(AddSurveyModel(**survey_data))
    mock_insert_one.assert_called_with(
        {
            "question": "any_question",
            "answers": [
                {"answer": "any_answer", "image": "any_image"},
                {"answer": "other_answer", "image": None},
            ],
            "date": datetime.utcnow(),
        }
    )


@freeze_time("2021-03-09")
def test_should_create_a_survey_on_add(sut: SurveyMongoRepo):
    survey_data = dict(
        question="any_question",
        answers=[
            dict(answer="any_answer", image="any_image"),
            dict(answer="other_answer", image=None),
        ],
    )
    sut.add(AddSurveyModel(**survey_data))
    survey = MOCK_COLLECTION.find_one()
    assert survey
    assert survey["_id"]
    assert survey["question"] == survey_data["question"]
    assert survey["answers"] == survey_data["answers"]
    assert survey["date"] == datetime.utcnow()
