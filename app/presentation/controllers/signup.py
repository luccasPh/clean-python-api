from ..protocols.http import Request, Response
from ..errors.missing_param_error import MissingParamError
from ..helpers.http_herlper import bad_request


class SignUpController:
    def handle(self, request: Request) -> Response:
        data = request.body
        if not data.get("name"):
            return bad_request(MissingParamError("name"))

        if not data.get("email"):
            return bad_request(MissingParamError("email"))
