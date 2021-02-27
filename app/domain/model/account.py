from dataclasses import dataclass


@dataclass
class AccountModel:
    id: str
    name: str
    email: str
    hashed_password: str
