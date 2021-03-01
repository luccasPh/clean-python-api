from ..protocols.controller import Controller
from ..protocols.http import HttpRequest, HttpResponse
from ..errors.missing_param_error import MissingParamError
from ..errors.invalid_param_error import InvalidParamError
from ..protocols.email_validator import EmailValidator
from ..helpers.http_herlper import bad_request


class LoginController(Controller):
    def __init__(self, email_validator: EmailValidator):
        self._email_validator = email_validator

    def handle(self, request: HttpRequest) -> HttpResponse:
        data = request.body
        if not data.get("email"):
            return bad_request(MissingParamError("email"))

        if not data.get("password"):
            return bad_request(MissingParamError("password"))

        is_valid = self._email_validator.is_valid(data.get("email"))
        if not is_valid:
            return bad_request(InvalidParamError("email"))