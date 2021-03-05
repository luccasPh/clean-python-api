from app.domain import AddSurvey
from ...protocols.controller import Controller, HttpRequest, HttpResponse
from ...protocols.validation import Validation
from ...helpers.http.http_herlper import bad_request


class AddSurveyController(Controller):
    def __init__(self, validation: Validation, add_survey: AddSurvey):
        self._validation = validation
        self._add_survey = add_survey

    def handle(self, request: HttpRequest) -> HttpResponse:
        data = request.body
        is_error = self._validation.validate(data)
        if is_error:
            return bad_request(is_error)
        self._add_survey.add(data)
