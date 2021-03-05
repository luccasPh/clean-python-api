from abc import ABC, abstractmethod


class DbSearchByField(ABC):
    @abstractmethod
    def search_by_field(self, field: str, value: str) -> bool:
        """Abstract method for check if already exist a value on specific field"""
