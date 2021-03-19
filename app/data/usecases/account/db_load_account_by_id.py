from app.domain import LoadAccountById, AccountModel
from ...protocols.cryptography.decrypter import Decrypter
from ...protocols.repositories.account.load_account_by_id_repo import (
    LoadAccountByIdRepo,
)


class DbLoadAccountById(LoadAccountById):
    def __init__(
        self, decrypter: Decrypter, load_account_by_id_repo: LoadAccountByIdRepo
    ):
        self._decrypter = decrypter
        self._load_account_by_id_repo = load_account_by_id_repo

    def load(self, access_token: str, role: str = None) -> AccountModel:
        account_id = self._decrypter.decrypt(access_token)
        if account_id:
            account = self._load_account_by_id_repo.load_by_id(account_id, role)
            if account:
                return account
