import jwt

from app.data import Encrypter, Decrypter


class JwtAdapter(Encrypter, Decrypter):
    def __init__(self, secret: str, algorithm: str):
        self._secret = secret
        self._algorithm = algorithm

    def encrypt(self, value: str) -> str:
        return jwt.encode(dict(id=value), self._secret, algorithm=self._algorithm)

    def decrypt(self, value: str) -> str:
        return jwt.decode(value, self._secret, algorithms=[self._algorithm])
