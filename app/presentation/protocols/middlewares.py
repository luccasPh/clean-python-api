from abc import ABC, abstractmethod

from .http import HttpResponse, HttpRequest


class Middleware(ABC):
    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse:
        """Abstract method for apply a middleware to router"""
