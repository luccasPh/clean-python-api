import traceback

from app.domain import AddAccount
from app.domain import AddAccountModel
from app.main import log_controller_handler
from ..protocols.http import HttpRequest, HttpResponse
from ..protocols.controller import Controller
from ..errors.server_error import ServerError
from ..helpers.http.http_herlper import bad_request, server_error, no_content
from ..protocols.validation import Validation


class SignUpController(Controller):
    def __init__(self, add_account: AddAccount, validation: Validation):
        self._add_account = add_account
        self._validation = validation

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            data = request.body
            is_error = self._validation.validate(data)
            if is_error:
                return bad_request(is_error)

            data.pop("password_confirmation")
            self._add_account.add(AddAccountModel(**data))

            return no_content()

        except Exception:
            return server_error(ServerError(), traceback.format_exc())
