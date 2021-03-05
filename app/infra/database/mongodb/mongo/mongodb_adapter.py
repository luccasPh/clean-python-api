from pymongo.collection import Collection

from app.validations import DbSearchByField


class MongoDbAdapter(DbSearchByField):
    def __init__(self, collection: Collection):
        self._collection = collection

    def search_by_field(self, field: str, value: str) -> bool:
        self._collection.find({field: value})
