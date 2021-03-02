from app.domain import Authentication, AuthenticationModel
from app.data import (
    LoadAccountByEmailRepo,
    HashComparer,
    TokenGenerator,
    UpdateAccessTokenRepo,
)


class DbAuthentication(Authentication):
    def __init__(
        self,
        load_account_by_email_repo: LoadAccountByEmailRepo,
        hash_comparer: HashComparer,
        token_generator: TokenGenerator,
        update_access_token_repo: UpdateAccessTokenRepo,
    ):
        self._load_account_by_email_repo = load_account_by_email_repo
        self._hash_comparer = hash_comparer
        self._token_generator = token_generator
        self._update_access_token_repo = update_access_token_repo

    def auth(self, authentication: AuthenticationModel) -> str:
        account = self._load_account_by_email_repo.load(authentication.email)
        if account:
            result = self._hash_comparer.compare(
                authentication.password, account.hashed_password
            )
            if result:
                access_token = self._token_generator.generate(account.id)
                self._update_access_token_repo.update(account.id, access_token)
                return access_token
