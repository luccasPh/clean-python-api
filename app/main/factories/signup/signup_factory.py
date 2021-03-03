from app.data import DbAddAccount
from app.infra import BcryptAdapter, AccountMongoRepo, get_collection
from app.presentation import SignUpController
from .signup_validation import make_signup_validation


def make_signup_controller():
    salt = b"$2b$12$9ITqN6psxZRjP8hN04j8Be"
    account_collection = get_collection("accounts")
    bcrypt_adapter = BcryptAdapter(salt)
    account_mongo_repo = AccountMongoRepo(account_collection)
    db_add_account = DbAddAccount(bcrypt_adapter, account_mongo_repo)
    return SignUpController(db_add_account, make_signup_validation())
