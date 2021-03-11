from app.domain import LoadSurveyById
from ...protocols.http import HttpRequest, HttpResponse
from ...protocols.controller import Controller


class SaveSurveyResultController(Controller):
    def __init__(self, load_survey_by_id: LoadSurveyById):
        self._load_survey_by_id = load_survey_by_id

    def handle(self, request: HttpRequest) -> HttpResponse:
        self._load_survey_by_id.load_by_id(request.params)
