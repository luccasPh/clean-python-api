from app.presentation import LoginController
from app.data import DbAuthentication
from app.infra import BcryptAdapter, JwtAdapter, AccountMongoRepo, get_collection
from app.main import env
from .login_validation import make_login_validation


def make_login_controller():
    salt = b"$2b$12$9ITqN6psxZRjP8hN04j8Be"
    bcrypt_adapter = BcryptAdapter(salt)
    jwt_adapter = JwtAdapter(env.JWT_SECRET_KEY)
    account_mongo_repo = AccountMongoRepo(get_collection("accounts"))
    db_authentication = DbAuthentication(
        load_account_by_email_repo=account_mongo_repo,
        hash_comparer=bcrypt_adapter,
        encrypter=jwt_adapter,
        update_access_token_repo=account_mongo_repo,
    )
    return LoginController(db_authentication, make_login_validation())