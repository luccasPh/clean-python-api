from bcrypt import hashpw, checkpw

from app.data import Hasher, HashComparer


class BcryptAdapter(Hasher, HashComparer):
    def __init__(self, salt: bytes):
        self._salt = salt

    def hash(self, value: str) -> str:
        hash = hashpw(value.encode("utf-8"), self._salt)
        return hash.decode("utf-8")

    def compare(self, value: str, hash: str) -> bool:
        return checkpw(value.encode("utf-8"), hash.encode("utf-8"))
