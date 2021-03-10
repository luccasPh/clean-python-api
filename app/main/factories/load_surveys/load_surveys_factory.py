from app.data import DbLoadSurveys
from app.infra import SurveyMongoRepo, get_collection
from app.presentation import LoadSurveysController


def make_load_surveys_controller():
    survey_collection = get_collection("surveys")
    load_surveys_repo = SurveyMongoRepo(survey_collection)
    db_load_surveys = DbLoadSurveys(load_surveys_repo)
    return LoadSurveysController(db_load_surveys)
