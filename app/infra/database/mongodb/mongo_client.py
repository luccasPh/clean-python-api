from pymongo.collection import Collection
from pymongo import MongoClient

from app.main import env


def get_collection(name: str) -> Collection:
    client = MongoClient(env.MONGO_URL)
    db = client["clean_python_api"]
    return db[name]
