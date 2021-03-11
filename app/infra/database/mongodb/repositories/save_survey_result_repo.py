from datetime import datetime
from pymongo.collection import Collection, ReturnDocument

from app.domain import SurveyResultModel, SaveSurveyResultModel
from app.data import SaveSurveyResultRepo


class SaveSurveyResultMongoRepo(SaveSurveyResultRepo):
    def __init__(
        self,
        survey_collection: Collection,
        survey_result_collection: Collection,
        account_collection: Collection,
    ):
        self._survey_collection = survey_collection
        self._survey_result_collection = survey_result_collection
        self._account_collection = account_collection

    def save(self, data: SaveSurveyResultModel) -> SurveyResultModel:
        survey_result = self._survey_result_collection.find_one_and_update(
            {"survey_id": data.survey_id, "account_id": data.account_id},
            {"$set": {"answer": data.answer, "date": datetime.utcnow()}},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        survey_result["id"] = str(survey_result.pop("_id"))
        return SurveyResultModel(**survey_result)
