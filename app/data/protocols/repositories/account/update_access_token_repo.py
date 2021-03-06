from abc import ABC, abstractmethod


class UpdateAccessTokenRepo(ABC):
    @abstractmethod
    def update_access_token(self, id: str, access_token: str):
        """Abstract method for update an account access token on db"""
