from abc import ABC, abstractmethod


class Validation(ABC):
    @abstractmethod
    def validate(self, input):
        """Abstract method for valid inputs"""
