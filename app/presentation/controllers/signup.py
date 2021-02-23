from ..protocols.http import Request, Response
from ..errors.missing_param_error import MissingParamError
from ..helpers.http_herlper import bad_request


class SignUpController:
    def handle(self, request: Request) -> Response:
        data = request.body
        required_fields = ("name", "email", "password")
        for field in required_fields:
            if not data.get(field):
                return bad_request(MissingParamError(field))
