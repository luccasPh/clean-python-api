from datetime import datetime
from pymongo.collection import Collection
from bson.objectid import ObjectId

from app.domain import SurveyResultModel, SaveSurveyResultModel
from app.data import SaveSurveyResultRepo
from ..mongo.pipeline_factory import make_pipeline


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
        pipeline = make_pipeline(survey_id)
        survey_result = self._survey_result_collection.aggregate(pipeline)
        return list(survey_result)[0]
