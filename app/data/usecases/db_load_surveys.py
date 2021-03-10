from app.data import LoadSurveysRepo


class DbLoadSurveys:
    def __init__(self, load_surveys_repo: LoadSurveysRepo):
        self._load_surveys_repo = load_surveys_repo

    def load(self):
        self._load_surveys_repo.load_all()
