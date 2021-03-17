import traceback

from app.domain import LoadSurveyById
from ...helpers.http.http_herlper import forbidden, server_error
from ...protocols.http import HttpRequest, HttpResponse
from ...protocols.controller import Controller
from ...errors.invalid_param_error import InvalidParamError
from ...errors.server_error import ServerError


class LoadSurveyResultController(Controller):
    def __init__(self, load_survey_by_id: LoadSurveyById):
        self._load_survey_by_id = load_survey_by_id

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            survey_id = request.params.get("survey_id")
            survey = self._load_survey_by_id.load_by_id(survey_id)
            if not survey:
                return forbidden(InvalidParamError("survey_id"))
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
