import traceback

from app.domain import LoadSurveyById, SaveSurveyResult, SaveSurveyResultModel
from app.main.decorators.log import log_controller_handler
from ...protocols.http import HttpRequest, HttpResponse
from ...protocols.controller import Controller
from ...helpers.http.http_herlper import forbidden, server_error
from ...errors.invalid_param_error import InvalidParamError
from ...errors.server_error import ServerError


class SaveSurveyResultController(Controller):
    def __init__(
        self, load_survey_by_id: LoadSurveyById, save_survey_result: SaveSurveyResult
    ):
        self._load_survey_by_id = load_survey_by_id
        self._save_survey_result = save_survey_result

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            survey_id = request.params.get("survey_id")
            answer = request.body.get("answer")
            account_id = request.account_id
            survey = self._load_survey_by_id.load_by_id(survey_id)
            if survey:
                if any(answers.answer == answer for answers in survey.answers):
                    data = dict(
                        survey_id=survey_id,
                        account_id=account_id,
                        answer=answer,
                    )
                    self._save_survey_result.save(SaveSurveyResultModel(**data))
                else:
                    return forbidden(InvalidParamError("answer"))
            else:
                return forbidden(InvalidParamError("survey_id"))
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
