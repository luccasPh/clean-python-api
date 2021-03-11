from app.presentation import SaveSurveyResultController
from app.infra import SaveSurveyResultMongoRepo, SurveyMongoRepo
from app.data import DbSaveSurveyResult

from app.infra import get_collection as get_collection_surveys
from app.infra import get_collection as get_collection_survey_results
from app.infra import get_collection as get_collection_accounts


def make_save_survey_result_controller():
    survey_collection = get_collection_surveys("surveys")
    survey_result_collection = get_collection_survey_results("survey_results")
    account_collection = get_collection_accounts("accounts")
    survey_result_repo = SaveSurveyResultMongoRepo(
        survey_collection, survey_result_collection, account_collection
    )
    db_save_survey_result = DbSaveSurveyResult(survey_result_repo)
    load_survey_by_id = SurveyMongoRepo(survey_collection)
    return SaveSurveyResultController(load_survey_by_id, db_save_survey_result)