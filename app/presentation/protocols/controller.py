from abc import ABC, abstractmethod

from .http import HttpRequest, HttpResponse


class Controller(ABC):
    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse:
        """Abstract method for handling a request"""
