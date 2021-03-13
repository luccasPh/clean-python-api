from datetime import datetime
from pymongo.collection import Collection
from bson.objectid import ObjectId

from app.domain import SurveyResultModel, SaveSurveyResultModel
from app.data import SaveSurveyResultRepo
from ..mongo.pipeline_builder import PipelineBuilder


class SaveSurveyResultMongoRepo(SaveSurveyResultRepo):
    def __init__(
        self,
        survey_collection: Collection,
        survey_result_collection: Collection,
    ):
        self._survey_collection = survey_collection
        self._survey_result_collection = survey_result_collection

    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        self._survey_result_collection.find_one_and_update(
            {
                "survey_id": ObjectId(data.survey_id),
                "account_id": ObjectId(data.account_id),
            },
            {"$set": {"answer": data.answer, "date": datetime.utcnow()}},
            upsert=True,
        )
        survey_result = self._load_by_survey_id(data.survey_id)
        survey_result["survey_id"] = str(survey_result["survey_id"])
        return SurveyResultModel(**survey_result)

    def _load_by_survey_id(self, survey_id: str) -> dict:
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
        survey_result = self._survey_result_collection.aggregate(pipeline)
        return list(survey_result)[0]
