from app.data import DbAddSurvey
from app.infra import SurveyMongoRepo, get_collection
from app.presentation import AddSurveyController
from .add_survey_validation import make_add_survey_validation


def make_add_survey_controller():
    survey_collection = get_collection("surveys")
    survey_mongo_repo = SurveyMongoRepo(survey_collection)
    db_add_survey = DbAddSurvey(survey_mongo_repo)
    return AddSurveyController(make_add_survey_validation(), db_add_survey)
