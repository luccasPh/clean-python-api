import traceback
from dataclasses import asdict

from app.domain import LoadSurveys
from app.main.decorators.log import log_controller_handler
from ...protocols.controller import Controller, HttpRequest, HttpResponse
from ...errors.server_error import ServerError
from ...helpers.http.http_herlper import no_content, ok, server_error


class LoadSurveysController(Controller):
    def __init__(self, load_surveys: LoadSurveys):
        self._load_surveys = load_surveys

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            surveys = self._load_surveys.load()
            surveys = list(map(lambda survey: asdict(survey), surveys))
            if len(surveys) == 0:
                return no_content()
            else:
                return ok(surveys)
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
