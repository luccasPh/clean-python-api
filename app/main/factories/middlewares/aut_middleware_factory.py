from datetime import datetime, timedelta

from app.presentation import AuthMiddleware
from app.data import DbLoadAccountById
from app.infra import AccountMongoRepo, JwtAdapter, get_collection
from app.main.config import env


def make_auth_middleware(role: str = None):
    account_collection = get_collection("accounts")
    load_account_by_id_repo = AccountMongoRepo(account_collection)
    decrypter = JwtAdapter(
        secret=env.JWT_SECRET_KEY,
        expiration_time=datetime.utcnow() + timedelta(hours=env.JWT_EXPIRATION_TIME),
        algorithm="HS256",
    )
    db_load_account_by_token = DbLoadAccountById(decrypter, load_account_by_id_repo)

    return AuthMiddleware(load_account_by_id=db_load_account_by_token, role=role)
