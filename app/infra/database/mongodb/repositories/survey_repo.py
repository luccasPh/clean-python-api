from dataclasses import asdict
from pymongo.collection import Collection

from app.domain import AddSurveyModel
from app.data import AddSurveyRepo


class SurveyMongoRepo(AddSurveyRepo):
    def __init__(self, survey_collection: Collection):
        self._survey_collection = survey_collection

    def add(self, data: AddSurveyModel):
        self._survey_collection.insert_one(asdict(data))
