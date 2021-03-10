from app.domain import AddSurvey, AddSurveyModel
from app.data import AddSurveyRepo


class DbAddSurvey(AddSurvey):
    def __init__(self, add_survey_repo: AddSurveyRepo):
        self._add_survey = add_survey_repo

    def add(self, data: AddSurveyModel):
        self._add_survey.add(data)
