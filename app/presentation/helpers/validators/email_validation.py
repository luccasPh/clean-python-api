from app.data import LoadAccountByEmailRepo
from ...protocols.validation import Validation
from ...errors.invalid_param_error import InvalidParamError
from ...protocols.email_validator import EmailValidator


class EmailValidation(Validation):
    def __init__(
        self,
        field_name: str,
        email_validator: EmailValidator,
        load_account_by_email_repo_stub: LoadAccountByEmailRepo,
    ):
        self.field_name = field_name
        self._email_validator = email_validator
        self._load_account_by_email_repo_stub = load_account_by_email_repo_stub

    def validate(self, input):
        is_valid = self._email_validator.is_valid(input[self.field_name])
        if not is_valid:
            return InvalidParamError(self.field_name)

        self._load_account_by_email_repo_stub.load_by_email(input[self.field_name])

    def __str__(self):
        return f"EmailValidation: {self.field_name}"
