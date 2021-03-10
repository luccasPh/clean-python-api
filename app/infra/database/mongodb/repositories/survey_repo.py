from dataclasses import asdict
from typing import Union
from pymongo.collection import Collection
from datetime import datetime

from app.domain import AddSurveyModel, SurveyModel
from app.data import AddSurveyRepo, LoadSurveysRepo


class SurveyMongoRepo(AddSurveyRepo, LoadSurveysRepo):
    def __init__(self, survey_collection: Collection):
        self._survey_collection = survey_collection

    def add(self, data: AddSurveyModel):
        add_survey = asdict(data)
        add_survey["date"] = datetime.utcnow()
        self._survey_collection.insert_one(add_survey)

    def load_all(self) -> Union[list[SurveyModel], None]:
        documents = list(self._survey_collection.find())
        surveys = []
        for document in documents:
            document["id"] = document.pop("_id")
            surveys.append(SurveyModel(**document))
        return surveys
