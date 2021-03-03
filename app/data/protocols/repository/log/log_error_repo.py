from abc import ABC, abstractmethod


class LogErrorRepo(ABC):
    @abstractmethod
    def log(self, value: str):
        """Abstract method for save errors traceback on database"""
