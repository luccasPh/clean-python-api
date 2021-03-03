import jwt

from app.data import Encrypter


class JwtAdapter(Encrypter):
    def __init__(self, secret: str):
        self._secret = secret

    def encrypt(self, value: str) -> str:
        jwt.encode(dict(id=value), self._secret)
