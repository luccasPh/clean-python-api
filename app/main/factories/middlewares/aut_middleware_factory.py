from app.presentation import AuthMiddleware
from app.data import DbLoadAccountByToken
from app.infra import AccountMongoRepo, JwtAdapter, get_collection
from app.main.config import env


def make_auth_middleware(role: str = None):
    decrypter = JwtAdapter(env.JWT_SECRET_KEY)
    load_account_by_token_repo = AccountMongoRepo(get_collection("accounts"))
    db_load_account_by_token = DbLoadAccountByToken(
        decrypter, load_account_by_token_repo
    )
    return AuthMiddleware(db_load_account_by_token, role)
