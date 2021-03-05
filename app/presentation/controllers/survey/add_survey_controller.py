from ...protocols.controller import Controller, HttpRequest, HttpResponse
from ...protocols.validation import Validation


class AddSurveyController(Controller):
    def __init__(self, validation: Validation):
        self._validation = validation

    def handle(self, request: HttpRequest) -> HttpResponse:
        self._validation.validate(request.body)
