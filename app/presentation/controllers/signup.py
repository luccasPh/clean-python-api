from ..protocols.http import Request, Response
from ..protocols.controller import Controller
from ..errors.missing_param_error import MissingParamError
from ..helpers.http_herlper import bad_request


class SignUpController(Controller):
    def handle(self, request: Request) -> Response:
        data = request.body
        required_fields = ("name", "email", "password", "password_confirmation")
        for field in required_fields:
            if not data.get(field):
                return bad_request(MissingParamError(field))
