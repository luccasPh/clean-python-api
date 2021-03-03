from app.domain import Authentication, AuthenticationModel
from app.data import (
    LoadAccountByEmailRepo,
    HashComparer,
    Encrypter,
    UpdateAccessTokenRepo,
)


class DbAuthentication(Authentication):
    def __init__(
        self,
        load_account_by_email_repo: LoadAccountByEmailRepo,
        hash_comparer: HashComparer,
        encrypter: Encrypter,
        update_access_token_repo: UpdateAccessTokenRepo,
    ):
        self._load_account_by_email_repo = load_account_by_email_repo
        self._hash_comparer = hash_comparer
        self._encrypter = encrypter
        self._update_access_token_repo = update_access_token_repo

    def auth(self, authentication: AuthenticationModel) -> str:
        account = self._load_account_by_email_repo.load_by_email(authentication.email)
        if account:
            result = self._hash_comparer.compare(
                authentication.password, account.hashed_password
            )
            if result:
                print("compare ok")
                access_token = self._encrypter.encrypt(account.id)
                self._update_access_token_repo.update_access_token(
                    account.id, access_token
                )
                return access_token
