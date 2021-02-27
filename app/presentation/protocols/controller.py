from abc import ABC, abstractmethod

from .http import Request, Response


class Controller(ABC):
    @abstractmethod
    def handle(self, request: Request) -> Response:
        """Abstract method for handling a request"""
