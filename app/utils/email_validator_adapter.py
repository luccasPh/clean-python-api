from validate_email import validate_email

from ..presentation.protocols.email_validator import EmailValidator


class EmailValidatorAdapter(EmailValidator):
    def is_valid(self, email: str) -> bool:
        return validate_email(email)
