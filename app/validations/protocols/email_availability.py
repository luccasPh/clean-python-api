from abc import ABC, abstractmethod
from typing import Any, Union


class EmailAvailability(ABC):
    @abstractmethod
    def load_by_email(self, email: str) -> Union[Any, None]:
        """Abstract method for check email availability"""
