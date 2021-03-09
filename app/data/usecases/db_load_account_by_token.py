from app.domain import LoadAccountByToken, AccountModel
from ..protocols.cryptography.decrypter import Decrypter
from ..protocols.repositories.account.load_account_by_token_repo import (
    LoadAccountByTokenRepo,
)


class DbLoadAccountByToken(LoadAccountByToken):
    def __init__(
        self, decrypter: Decrypter, load_account_by_token_repo: LoadAccountByTokenRepo
    ):
        self._decrypter = decrypter
        self._load_account_by_token_repo = load_account_by_token_repo

    def load(self, access_token: str, role: str = None) -> AccountModel:
        token = self._decrypter.decrypt(access_token)
        if token:
            account = self._load_account_by_token_repo.load_by_token(access_token, role)
            if account:
                return account
