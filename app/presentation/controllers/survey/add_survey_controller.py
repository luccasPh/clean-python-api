import traceback

from app.domain import AddSurvey, AddSurveyModel
from app.main.decorators.log import log_controller_handler
from ...protocols.controller import Controller, HttpRequest, HttpResponse
from ...protocols.validation import Validation
from ...errors.server_error import ServerError
from ...helpers.http.http_herlper import bad_request, server_error, no_content


class AddSurveyController(Controller):
    def __init__(self, validation: Validation, add_survey: AddSurvey):
        self._validation = validation
        self._add_survey = add_survey

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            data = request.body
            is_error = self._validation.validate(data)
            if is_error:
                return bad_request(is_error)
            self._add_survey.add(AddSurveyModel(**data))
            return no_content()
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
