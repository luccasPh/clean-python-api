import traceback

from app.domain import Authentication, AuthenticationModel
from app.main import log_controller_handler
from ..protocols.controller import Controller
from ..protocols.http import HttpRequest, HttpResponse
from ..errors.server_error import ServerError
from ..errors.unauthorized_error import UnauthorizedError
from ..protocols.validation import Validation
from ..helpers.http.http_herlper import bad_request, ok, server_error, unauthorized


class LoginController(Controller):
    def __init__(self, authentication: Authentication, validation: Validation):
        self._authentication = authentication
        self._validation = validation

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            data = request.body
            is_error = self._validation.validate(data)
            if is_error:
                return bad_request(is_error)

            access_token = self._authentication.auth(AuthenticationModel(**data))
            if not access_token:
                return unauthorized(UnauthorizedError())

            return ok(dict(access_token=access_token))
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
