from pymongo.collection import Collection
from datetime import datetime

from app.data import LogErrorRepo


class LogMongoRepo(LogErrorRepo):
    def __init__(self, log_collection: Collection):
        self._log_collection = log_collection

    def log(self, traceback: str):
        log_data = dict(traceback=traceback, date=datetime.utcnow())
        self._log_collection.insert_one(log_data)
