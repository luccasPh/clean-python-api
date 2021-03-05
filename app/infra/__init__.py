from app.infra.cryptography.bcrypt_adapter import BcryptAdapter
from app.infra.cryptography.jwt_adapter import JwtAdapter
from app.infra.database.mongodb.account.account_repo import AccountMongoRepo
from app.infra.database.mongodb.log.log_repo import LogMongoRepo
from app.infra.database.mongodb.mongo.mongo_client import get_collection
from app.infra.database.mongodb.mongo.mongodb_adapter import MongoDbAdapter
from app.infra.validators.email_validator_adapter import EmailValidatorAdapter
