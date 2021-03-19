import jwt
from datetime import datetime

from app.data import Encrypter, Decrypter


class JwtAdapter(Encrypter, Decrypter):
    def __init__(self, secret: str, expiration_time: datetime, algorithm: str):
        self._secret = secret
        self._expiration_time = expiration_time
        self._algorithm = algorithm

    def encrypt(self, value: str) -> str:
        return jwt.encode(
            {"id": value, "exp": self._expiration_time},
            self._secret,
            algorithm=self._algorithm,
        )

    def decrypt(self, value: str) -> str:
        decoded = jwt.decode(value, self._secret, algorithms=[self._algorithm])
        return decoded["id"]
