from pymongo.collection import Collection

from app.validations import DbSearchByField


class MongoDbAdapter(DbSearchByField):
    def __init__(self, collection: Collection):
        self._collection = collection

    def search_by_field(self, field: str, value: str) -> bool:
        result = self._collection.find_one({field: value})
        if result:
            return True
        else:
            return False
