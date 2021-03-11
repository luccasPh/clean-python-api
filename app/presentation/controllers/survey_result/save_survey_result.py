import traceback

from app.domain import LoadSurveyById
from app.main.decorators.log import log_controller_handler
from ...protocols.http import HttpRequest, HttpResponse
from ...protocols.controller import Controller
from ...helpers.http.http_herlper import forbidden, server_error
from ...errors.invalid_param_error import InvalidParamError
from ...errors.server_error import ServerError


class SaveSurveyResultController(Controller):
    def __init__(self, load_survey_by_id: LoadSurveyById):
        self._load_survey_by_id = load_survey_by_id

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            survey = self._load_survey_by_id.load_by_id(request.params)
            if not survey:
                return forbidden(InvalidParamError("survey_id"))
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
