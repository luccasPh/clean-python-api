import traceback
from dataclasses import asdict

from app.domain import AddAccount
from app.domain import AddAccountModel
from app.main import log_controller_handler
from ..protocols.http import HttpRequest, HttpResponse
from ..protocols.email_validator import EmailValidator
from ..protocols.controller import Controller
from ..errors.invalid_param_error import InvalidParamError
from ..errors.server_error import ServerError
from ..helpers.http.http_herlper import bad_request, server_error, ok
from ..helpers.validators.validation import Validation


class SignUpController(Controller):
    def __init__(
        self,
        email_validator: EmailValidator,
        add_account: AddAccount,
        validation: Validation,
    ):
        self._email_validator = email_validator
        self._add_account = add_account
        self._validation = validation

    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            data = request.body
            print(data)
            is_error = self._validation.validate(data)
            if is_error:
                return bad_request(is_error)

            if data.get("password") != data.get("password_confirmation"):
                return bad_request(InvalidParamError("password_confirmation"))

            is_valid = self._email_validator.is_valid(data.get("email"))
            if not is_valid:
                return bad_request(InvalidParamError("email"))

            data.pop("password_confirmation")
            account = self._add_account.add(AddAccountModel(**data))

            return ok(asdict(account))

        except Exception:
            return server_error(ServerError(), traceback.format_exc())
