from app.domain import LoadSurveyById
from ...protocols.http import HttpRequest, HttpResponse
from ...protocols.controller import Controller


class LoadSurveyResultController(Controller):
    def __init__(self, load_survey_by_id: LoadSurveyById):
        self._load_survey_by_id = load_survey_by_id

    def handle(self, request: HttpRequest) -> HttpResponse:
        survey_id = request.params.get("survey_id")
        self._load_survey_by_id.load_by_id(survey_id)
