from app.data import DbAddAccount
from app.utils.email_validator_adapter import EmailValidatorAdapter
from app.infra import BcryptAdapter, AccountMongoRepo, get_collection
from app.presentation import SignUpController


def make_signup_controller():
    salt = b"$2b$12$9ITqN6psxZRjP8hN04j8Be"
    account_collection = get_collection("accounts")
    email_validator_adapter = EmailValidatorAdapter(check_mx=False, skip_smtp=True)
    bcrypt_adapter = BcryptAdapter(salt)
    account_mongo_repo = AccountMongoRepo(account_collection)
    db_add_account = DbAddAccount(bcrypt_adapter, account_mongo_repo)
    return SignUpController(email_validator_adapter, db_add_account)
