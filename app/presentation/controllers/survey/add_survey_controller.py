from ...protocols.controller import Controller, HttpRequest, HttpResponse
from ...protocols.validation import Validation
from ...helpers.http.http_herlper import bad_request


class AddSurveyController(Controller):
    def __init__(self, validation: Validation):
        self._validation = validation

    def handle(self, request: HttpRequest) -> HttpResponse:
        is_error = self._validation.validate(request.body)
        if is_error:
            return bad_request(is_error)
