from app.domain import AddAccount, AddAccountModel, AccountModel
from ..protocols.cryptography.encrypter import Encrypter
from ..protocols.repository.add_account_repo import AddAccountRepo


class DbAddAccount(AddAccount):
    def __init__(self, encrypter: Encrypter, add_account_repo: AddAccountRepo):
        self._encrypter = encrypter
        self._add_account_repo = add_account_repo

    def add(self, data: AddAccountModel) -> AccountModel:
        hashed_password = self._encrypter.encrypt(data.password)
        data.password = hashed_password
        account = self._add_account_repo.add(data)
        return account
