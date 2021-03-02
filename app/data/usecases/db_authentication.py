from app.domain import Authentication, AuthenticationModel
from app.data import LoadAccountByEmailRepo, HashComparer, TokenGenerator


class DbAuthentication(Authentication):
    def __init__(
        self,
        load_account_by_email_repo: LoadAccountByEmailRepo,
        hash_comparer: HashComparer,
        token_generator: TokenGenerator,
    ):
        self._load_account_by_email_repo = load_account_by_email_repo
        self._hash_comparer = hash_comparer
        self._token_generator = token_generator

    def auth(self, authentication: AuthenticationModel) -> str:
        account = self._load_account_by_email_repo.load(authentication.email)
        if account:
            result = self._hash_comparer.compare(
                authentication.password, account.hashed_password
            )
            if result:
                return self._token_generator.generate(account.id)
