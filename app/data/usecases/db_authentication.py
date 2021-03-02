from app.domain import Authentication, AuthenticationModel
from app.data import LoadAccountByEmailRepo, HashComparer


class DbAuthentication(Authentication):
    def __init__(
        self,
        load_account_by_email_repo: LoadAccountByEmailRepo,
        hash_comparer: HashComparer,
    ):
        self._load_account_by_email_repo = load_account_by_email_repo
        self._hash_comparer = hash_comparer

    def auth(self, authentication: AuthenticationModel) -> str:
        account = self._load_account_by_email_repo.load(authentication.email)
        if account:
            self._hash_comparer.compare(
                authentication.password, account.hashed_password
            )
