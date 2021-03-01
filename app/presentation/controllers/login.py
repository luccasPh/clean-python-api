import traceback

from app.domain import Authentication
from ..protocols.controller import Controller
from ..protocols.http import HttpRequest, HttpResponse
from ..errors.missing_param_error import MissingParamError
from ..errors.invalid_param_error import InvalidParamError
from ..errors.server_error import ServerError
from ..protocols.email_validator import EmailValidator
from ..helpers.http_herlper import bad_request, server_error


class LoginController(Controller):
    def __init__(self, email_validator: EmailValidator, authentication: Authentication):
        self._email_validator = email_validator
        self._authentication = authentication

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            data = request.body
            required_fields = ("email", "password")
            for field in required_fields:
                if not data.get(field):
                    return bad_request(MissingParamError(field))

            is_valid = self._email_validator.is_valid(data.get("email"))
            if not is_valid:
                return bad_request(InvalidParamError("email"))

            self._authentication.auth(data)
        except Exception:
            return server_error(ServerError(), traceback.format_exc())
