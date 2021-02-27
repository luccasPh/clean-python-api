from app.domain import AddAccount, AddAccountModel, AccountModel
from ..protocols.encrypter import Encrypter


class DbAddAccount(AddAccount):
    def __init__(self, encrypter: Encrypter):
        self._encrypter = encrypter

    def add(self, data: AddAccountModel) -> AccountModel:
        self._encrypter.encrypt(data.password)
        return None
