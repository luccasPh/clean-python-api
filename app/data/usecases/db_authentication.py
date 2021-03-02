from app.domain import Authentication, AuthenticationModel
from app.data import LoadAccountByEmailRepo


class DbAuthentication(Authentication):
    def __init__(self, load_account_by_email_repo: LoadAccountByEmailRepo):
        self.load_account_by_email_repo = load_account_by_email_repo

    def auth(self, authentication: AuthenticationModel) -> str:
        self.load_account_by_email_repo.load(authentication.email)
