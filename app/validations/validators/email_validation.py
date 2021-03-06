from app.presentation import Validation, InvalidParamError
from ..protocols.email_validator import EmailValidator


class EmailValidation(Validation):
    def __init__(
        self,
        field_name: str,
        email_validator: EmailValidator,
    ):
        self.field_name = field_name
        self._email_validator = email_validator

    def validate(self, input):
        is_valid = self._email_validator.is_valid(input[self.field_name])
        if not is_valid:
            return InvalidParamError(self.field_name)

    def __str__(self):
        return f"EmailValidation: {self.field_name}"
