from app.domain import LoadAccountByToken, AccountModel
from ..protocols.cryptography.decrypter import Decrypter


class DbLoadAccountByToken(LoadAccountByToken):
    def __init__(self, decrypter: Decrypter):
        self._decrypter = decrypter

    def load_by_token(self, access_token: str, role: str = None) -> AccountModel:
        self._decrypter.decrypt(access_token)
