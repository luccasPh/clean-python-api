import traceback
from jwt.exceptions import PyJWTError

from app.domain.usecases.account.load_account_by_id import LoadAccountById
from app.main.decorators.log import log_controller_handler
from ..protocols.http import HttpRequest, HttpResponse
from ..protocols.middlewares import Middleware
from ..helpers.http.http_herlper import forbidden, ok, server_error, unauthorized
from ..errors.access_danied_error import AccessDaniedError
from ..errors.server_error import ServerError
from ..errors.unauthorized_error import UnauthorizedError


class AuthMiddleware(Middleware):
    def __init__(self, load_account_by_id: LoadAccountById, role: str = None):
        self._load_account_by_id = load_account_by_id
        self._role = role

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            access_token = (
                request.headers and request.headers.get("x-access-token") or None
            )
            if access_token:
                account = self._load_account_by_id.load(
                    access_token=access_token, role=self._role
                )
                if account:
                    return ok(account.id)

            return forbidden(AccessDaniedError())
        except PyJWTError:
            return unauthorized(UnauthorizedError())
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
