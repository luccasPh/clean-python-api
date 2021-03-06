from app.domain.usecases.load_account_by_token import LoadAccountByToken
from ..protocols.http import HttpRequest, HttpResponse
from ..protocols.middlewares import Middleware
from ..helpers.http.http_herlper import forbidden, ok
from ..errors.access_danied_error import AccessDaniedError


class AuthMiddleware(Middleware):
    def __init__(self, load_account_by_token: LoadAccountByToken):
        self._load_account_by_token = load_account_by_token

    def handle(self, request: HttpRequest) -> HttpResponse:

        access_token = request.headers and request.headers.get("x-access-token") or None
        if access_token:
            account = self._load_account_by_token.load_by_token(
                access_token=access_token
            )
            if account:
                return ok(account.id)

        return forbidden(AccessDaniedError())
