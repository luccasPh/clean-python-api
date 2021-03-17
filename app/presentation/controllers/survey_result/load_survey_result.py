import traceback
from dataclasses import asdict

from app.domain import LoadSurveyById, LoadSurveyResult
from ...helpers.http.http_herlper import forbidden, ok, server_error
from ...protocols.http import HttpRequest, HttpResponse
from ...protocols.controller import Controller
from ...errors.invalid_param_error import InvalidParamError
from ...errors.server_error import ServerError


class LoadSurveyResultController(Controller):
    def __init__(
        self, load_survey_by_id: LoadSurveyById, load_survey_result: LoadSurveyResult
    ):
        self._load_survey_by_id = load_survey_by_id
        self._load_survey_result = load_survey_result

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            survey_id = request.params.get("survey_id")
            survey = self._load_survey_by_id.load_by_id(survey_id)
            if survey:
                survey_result = self._load_survey_result.load(survey_id)
                return ok(asdict(survey_result))
            else:
                return forbidden(InvalidParamError("survey_id"))
        except Exception:
            print(traceback.format_exc())
            return server_error(ServerError(), traceback.format_exc())
