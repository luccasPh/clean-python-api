from app.domain import AddAccount
from app.domain import AddAccountModel
from ..protocols.http import Request, Response
from ..protocols.email_validator import EmailValidator
from ..protocols.controller import Controller
from ..errors.missing_param_error import MissingParamError
from ..errors.invalid_param_error import InvalidParamError
from ..errors.server_error import ServerError
from ..helpers.http_herlper import bad_request, server_error


class SignUpController(Controller):
    def __init__(self, email_validator: EmailValidator, add_account: AddAccount):
        self._email_validator = email_validator
        self._add_account = add_account

    def handle(self, request: Request) -> Response:
        try:
            data = request.body
            required_fields = ("name", "email", "password", "password_confirmation")
            for field in required_fields:
                if not data.get(field):
                    return bad_request(MissingParamError(field))

            if data.get("password") != data.get("password_confirmation"):
                return bad_request(InvalidParamError("password_confirmation"))

            is_valid = self._email_validator.is_valid(data.get("email"))
            if not is_valid:
                return bad_request(InvalidParamError("email"))

            data.pop("password_confirmation")
            account_in = AddAccountModel(**data)
            self._add_account.add(account_in)

        except Exception as error:
            print(error)
            return server_error(ServerError())
