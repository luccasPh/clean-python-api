from app.domain import Authentication, AuthenticationModel
from app.data import (
    LoadAccountByEmailRepo,
    HashComparer,
    Encrypter,
)


class DbAuthentication(Authentication):
    def __init__(
        self,
        load_account_by_email_repo: LoadAccountByEmailRepo,
        hash_comparer: HashComparer,
        encrypter: Encrypter,
    ):
        self._load_account_by_email_repo = load_account_by_email_repo
        self._hash_comparer = hash_comparer
        self._encrypter = encrypter

    def auth(self, authentication: AuthenticationModel) -> str:
        account = self._load_account_by_email_repo.load_by_email(authentication.email)
        if account:
            result = self._hash_comparer.compare(
                authentication.password, account.hashed_password
            )
            if result:
                access_token = self._encrypter.encrypt(account.id)
                return access_token
