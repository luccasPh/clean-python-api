from ..protocols.controller import Controller
from ..protocols.http import HttpRequest, HttpResponse
from ..errors.missing_param_error import MissingParamError
from ..helpers.http_herlper import bad_request


class LoginController(Controller):
    def handle(self, request: HttpRequest) -> HttpResponse:
        return bad_request(MissingParamError("email"))
