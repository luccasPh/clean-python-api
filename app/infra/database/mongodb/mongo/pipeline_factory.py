from app.main.config import env
from .pipeline_builder import PipelineBuilder
from bson.objectid import ObjectId


def make_pipeline(survey_id: str) -> dict:
    if env.ENVIRONMENT == "test":
        pipeline = (
            PipelineBuilder()
            .match({"survey_id": ObjectId(survey_id)})
            .group(
                {
                    "_id": 0,
                    "data": {"$push": "$$ROOT"},
                    "count": {"$sum": 1},
                }
            )
            .unwind({"path": "$data"})
            .lookup(
                {
                    "from": "surveys",
                    "localField": "data.survey_id",
                    "foreignField": "_id",
                    "as": "survey",
                }
            )
            .unwind({"path": "$survey"})
            .group(
                {
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
            )
            .unwind({"path": "$_id.answer"})
            .addFields(
                {
                    "_id.answer.count": "$count",
                    "_id.answer.percent": {
                        "$multiply": [{"$divide": ["$count", "$_id.total"]}, 100]
                    },
                }
            )
            .group(
                {
                    "_id": {
                        "survey_id": "$_id.survey_id",
                        "question": "$_id.question",
                        "date": "$_id.date",
                    },
                    "answers": {"$push": "$_id.answer"},
                }
            )
            .project(
                {
                    "_id": 0,
                    "survey_id": "$_id.survey_id",
                    "question": "$_id.question",
                    "date": "$_id.date",
                    "answers": "$answers",
                }
            )
            .build()
        )

    else:
        pipeline = (
            PipelineBuilder()
            .match({"survey_id": ObjectId(survey_id)})
            .group(
                {
                    "_id": 0,
                    "data": {"$push": "$$ROOT"},
                    "total": {"$sum": 1},
                }
            )
            .unwind({"path": "$data"})
            .lookup(
                {
                    "from": "surveys",
                    "localField": "data.survey_id",
                    "foreignField": "_id",
                    "as": "survey",
                }
            )
            .unwind({"path": "$survey"})
            .group(
                {
                    "_id": {
                        "survey_id": "$survey._id",
                        "question": "$survey.question",
                        "date": "$survey.date",
                        "total": "$total",
                        "answer": "$data.answer",
                        "answers": "$survey.answers",
                    },
                    "count": {"$sum": 1},
                }
            )
            .project(
                {
                    "_id": 0,
                    "survey_id": "$_id.survey_id",
                    "question": "$_id.question",
                    "date": "$_id.date",
                    "answers": {
                        "$map": {
                            "input": "$_id.answers",
                            "as": "item",
                            "in": {
                                "$mergeObjects": [
                                    "$$item",
                                    {
                                        "count": {
                                            "$cond": {
                                                "if": {
                                                    "$eq": [
                                                        "$$item.answer",
                                                        "$_id.answer",
                                                    ]
                                                },
                                                "then": "$count",
                                                "else": 0,
                                            }
                                        },
                                        "percent": {
                                            "$cond": {
                                                "if": {
                                                    "$eq": [
                                                        "$$item.answer",
                                                        "$_id.answer",
                                                    ]
                                                },
                                                "then": {
                                                    "$multiply": [
                                                        {
                                                            "$divide": [
                                                                "$count",
                                                                "$_id.total",
                                                            ]
                                                        },
                                                        100,
                                                    ]
                                                },
                                                "else": 0,
                                            }
                                        },
                                    },
                                ]
                            },
                        }
                    },
                }
            )
            .group(
                {
                    "_id": {
                        "survey_id": "$survey_id",
                        "question": "$question",
                        "date": "$date",
                    },
                    "answers": {"$push": "$answers"},
                }
            )
            .project(
                {
                    "_id": 0,
                    "survey_id": "$_id.survey_id",
                    "question": "$_id.question",
                    "date": "$_id.date",
                    "answers": {
                        "$reduce": {
                            "input": "$answers",
                            "initialValue": [],
                            "in": {"$concatArrays": ["$$value", "$$this"]},
                        }
                    },
                }
            )
            .unwind({"path": "$answers"})
            .group(
                {
                    "_id": {
                        "survey_id": "$survey_id",
                        "question": "$question",
                        "date": "$date",
                        "answer": "$answers.answer",
                        "image": "$answers.image",
                    },
                    "count": {"$sum": "$answers.count"},
                    "percent": {"$sum": "$answers.percent"},
                }
            )
            .project(
                {
                    "_id": 0,
                    "survey_id": "$_id.survey_id",
                    "question": "$_id.question",
                    "date": "$_id.date",
                    "answer": {
                        "answer": "$_id.answer",
                        "image": "$_id.image",
                        "count": "$count",
                        "percent": {"$trunc": ["$percent", 1]},
                    },
                }
            )
            .sort({"answer.count": -1})
            .group(
                {
                    "_id": {
                        "survey_id": "$survey_id",
                        "question": "$question",
                        "date": "$date",
                    },
                    "answers": {"$push": "$answer"},
                }
            )
            .project(
                {
                    "_id": 0,
                    "survey_id": "$_id.survey_id",
                    "question": "$_id.question",
                    "date": "$_id.date",
                    "answers": "$answers",
                }
            )
            .build()
        )

    return pipeline
