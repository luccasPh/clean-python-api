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


@patch.object(MOCK_COLLECTION, "insert_one")
def test_should_raise_exception_if_collection_insert_raise_on_add(
    mock_insert_one: MagicMock, sut: SurveyMongoRepo
):
    mock_insert_one.side_effect = Exception()
    survey_data = dict(
        question="any_question",
        answers=[
            dict(answer="any_answer", image="any_image"),
            dict(answer="other_answer", image=None),
        ],
    )
    with pytest.raises(Exception) as excinfo:
        sut.add(AddSurveyModel(**survey_data))
    assert type(excinfo.value) is Exception


@freeze_time("2021-03-09")
def test_should_returns_surveys_on_load_all(sut: SurveyMongoRepo):
    MOCK_COLLECTION.insert_many(
        [
            dict(
                question="any_question",
                answers=[
                    dict(answer="any_answer", image="any_image"),
                ],
                date=datetime.utcnow(),
            ),
            dict(
                question="other_question",
                answers=[
                    dict(answer="other_answer", image="other_image"),
                ],
                date=datetime.utcnow(),
            ),
        ]
    )
    surveys = sut.load_all()
    assert len(surveys) == 2
    assert surveys[0].question == "any_question"
    assert surveys[1].question == "other_question"
