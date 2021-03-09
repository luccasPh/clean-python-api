from app.domain import LoadSurveys
from ...protocols.controller import Controller, HttpRequest, HttpResponse


class LoadSurveysController(Controller):
    def __init__(self, load_surveys: LoadSurveys):
        self._load_surveys = load_surveys

    def handle(self, request: HttpRequest) -> HttpResponse:
        self._load_surveys.load()
