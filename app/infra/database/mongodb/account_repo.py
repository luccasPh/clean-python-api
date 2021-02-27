from pymongo.collection import Collection
from dataclasses import asdict

from app.domain import AccountModel, AddAccountModel
from app.data import AddAccountRepo


class AccountMongoRepo(AddAccountRepo):
    def __init__(self, account_collection: Collection):
        self._account_collection = account_collection

    def add(self, data: AddAccountModel) -> AccountModel:
        account_data = asdict(data)
        account_data["hashed_password"] = account_data.pop("password")
        obj_id = self._account_collection.insert_one(account_data).inserted_id
        account = self._account_collection.find_one({"_id": obj_id})
        account["id"] = account.pop("_id")
        return AccountModel(**account)
