from typing import Union
from pymongo.collection import Collection
from bson.objectid import ObjectId
from dataclasses import asdict

from app.domain import AccountModel, AddAccountModel
from app.data import (
    AddAccountRepo,
    LoadAccountByEmailRepo,
    LoadAccountByIdRepo,
)


class AccountMongoRepo(
    AddAccountRepo,
    LoadAccountByEmailRepo,
    LoadAccountByIdRepo,
):
    def __init__(self, account_collection: Collection):
        self._account_collection = account_collection

    def add(self, data: AddAccountModel):
        account_data = asdict(data)
        account_data["hashed_password"] = account_data.pop("password")
        self._account_collection.insert_one(account_data).inserted_id

    def load_by_email(self, email: str) -> AccountModel:
        account = self._account_collection.find_one({"email": email})
        if account:
            account["id"] = str(account.pop("_id"))
            return AccountModel(
                id=account["id"],
                name=account["name"],
                email=account["email"],
                hashed_password=account["hashed_password"],
            )

    def load_by_id(self, id: str, role: str = None) -> Union[AccountModel, None]:
        account = self._account_collection.find_one(
            {"_id": ObjectId(id), "$or": [{"role": role}, {"role": "admin"}]}
        )
        if account:
            account["id"] = str(account.pop("_id"))
            if "role" in account:
                account.pop("role")
            return AccountModel(**account)
