from bson.objectid import ObjectId

from app.infra.database.mongodb.mongo.pipeline_factory import make_pipeline
from app.main.config import env


def test_should_pipeline_factory_returns_a_pipeline_test():
    env.ENVIRONMENT = "test"
    survey_id = ObjectId()
    pipeline = make_pipeline(survey_id)
    expected = [
        {"$match": {"survey_id": ObjectId(survey_id)}},
        {"$group": {"_id": 0, "data": {"$push": "$$ROOT"}, "count": {"$sum": 1}}},
        {"$unwind": {"path": "$data"}},
        {
            "$lookup": {
                "from": "surveys",
                "localField": "data.survey_id",
                "foreignField": "_id",
                "as": "survey",
            }
        },
        {"$unwind": {"path": "$survey"}},
        {
            "$group": {
                "_id": {
                    "survey_id": "$survey._id",
                    "question": "$survey.question",
                    "date": "$survey.date",
                    "total": "$count",
                    "answer": {
                        "$filter": {
                            "input": "$survey.answers",
                            "as": "item",
                            "cond": {"$eq": ["$$item.answer", "$data.answer"]},
                        }
                    },
                },
                "count": {"$sum": 1},
            }
        },
        {"$unwind": {"path": "$_id.answer"}},
        {
            "$addFields": {
                "_id.answer.count": "$count",
                "_id.answer.percent": {
                    "$multiply": [{"$divide": ["$count", "$_id.total"]}, 100]
                },
            }
        },
        {"$sort": {"answer.count": -1}},
        {
            "$group": {
                "_id": {
                    "survey_id": "$_id.survey_id",
                    "question": "$_id.question",
                    "date": "$_id.date",
                },
                "answers": {"$push": "$_id.answer"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "survey_id": "$_id.survey_id",
                "question": "$_id.question",
                "date": "$_id.date",
                "answers": "$answers",
            }
        },
    ]
    assert pipeline == expected
