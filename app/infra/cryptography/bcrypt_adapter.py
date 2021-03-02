from bcrypt import hashpw

from app.data import Hasher


class BcryptAdapter(Hasher):
    def __init__(self, salt: bytes):
        self._salt = salt

    def hash(self, value: str) -> str:
        hash = hashpw(value.encode("utf-8"), self._salt)
        return hash.decode("utf-8")
