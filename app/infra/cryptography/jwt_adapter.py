import jwt

from app.data import Encrypter, Decrypter


class JwtAdapter(Encrypter, Decrypter):
    def __init__(self, secret: str):
        self._secret = secret

    def encrypt(self, value: str) -> str:
        return jwt.encode(dict(id=value), self._secret)

    def decrypt(self, value: str) -> str:
        jwt.decode(value, "secret")
