from app.domain import LoadSurveyById
from ...protocols.http import HttpRequest, HttpResponse
from ...protocols.controller import Controller
from ...helpers.http.http_herlper import forbidden
from ...errors.invalid_param_error import InvalidParamError


class SaveSurveyResultController(Controller):
    def __init__(self, load_survey_by_id: LoadSurveyById):
        self._load_survey_by_id = load_survey_by_id

    def handle(self, request: HttpRequest) -> HttpResponse:
        survey = self._load_survey_by_id.load_by_id(request.params)
        if not survey:
            return forbidden(InvalidParamError("survey_id"))
