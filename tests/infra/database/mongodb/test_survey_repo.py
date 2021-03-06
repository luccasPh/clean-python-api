import mongomock
import pytest

# from mock import patch, MagicMock
# from bson.objectid import ObjectId

from app.infra import SurveyMongoRepo
from app.domain import AddSurveyModel


MOCK_COLLECTION = mongomock.MongoClient().db.collection


@pytest.fixture
def sut():
    yield SurveyMongoRepo(MOCK_COLLECTION)
    MOCK_COLLECTION.drop()


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
