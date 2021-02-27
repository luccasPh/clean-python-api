from bcrypt import hashpw

from app.data import Encrypter


class BcryptAdapter(Encrypter):
    def __init__(self, salt: bytes):
        self._salt = salt

    def encrypt(self, value: str) -> str:
        hash = hashpw(value.encode("utf-8"), self._salt)
        return hash.decode("utf-8")
