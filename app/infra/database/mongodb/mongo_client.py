from pymongo.collection import Collection
from pymongo import MongoClient


def get_collection(name: str) -> Collection:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.clean_python_api
    return db[name]
