from bcrypt import hashpw

from app.data import Encrypter


class BcryptAdapter(Encrypter):
    def __init__(self, salt: int):
        self._salt = salt

    def encrypt(self, value: str) -> str:
        hashpw(value, self._salt)
