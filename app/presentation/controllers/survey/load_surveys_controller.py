from dataclasses import asdict

from app.domain import LoadSurveys
from ...protocols.controller import Controller, HttpRequest, HttpResponse
from ...helpers.http.http_herlper import ok


class LoadSurveysController(Controller):
    def __init__(self, load_surveys: LoadSurveys):
        self._load_surveys = load_surveys

    def handle(self, request: HttpRequest) -> HttpResponse:
        surveys_model = self._load_surveys.load()
        surveys = []
        if surveys_model:
            for survey in surveys_model:
                surveys.append(asdict(survey))

        return ok(surveys)
