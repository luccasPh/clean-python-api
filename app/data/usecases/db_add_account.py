from app.domain import AddAccount, AddAccountModel, AccountModel
from ..protocols.cryptography.hasher import Hasher
from ..protocols.repository.add_account_repo import AddAccountRepo


class DbAddAccount(AddAccount):
    def __init__(self, Hasher: Hasher, add_account_repo: AddAccountRepo):
        self._hasher = Hasher
        self._add_account_repo = add_account_repo

    def add(self, data: AddAccountModel) -> AccountModel:
        hashed_password = self._hasher.hash(data.password)
        data.password = hashed_password
        account = self._add_account_repo.add(data)
        return account
