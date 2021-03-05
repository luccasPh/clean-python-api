from app.presentation import Validation, InvalidParamError, EmailInUseError
from ..protocols.email_availability import EmailAvailability
from ..protocols.email_validator import EmailValidator


class EmailValidation(Validation):
    def __init__(
        self,
        field_name: str,
        email_validator: EmailValidator,
        email_availability: EmailAvailability,
    ):
        self.field_name = field_name
        self._email_validator = email_validator
        self._email_availability = email_availability

    def validate(self, input):
        is_valid = self._email_validator.is_valid(input[self.field_name])
        if not is_valid:
            return InvalidParamError(self.field_name)

        account = self._email_availability.load_by_email(input[self.field_name])
        if account:
            return EmailInUseError()

    def __str__(self):
        return f"EmailValidation: {self.field_name}"
