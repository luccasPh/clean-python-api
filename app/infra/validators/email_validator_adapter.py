from validate_email import validate_email

from app.validations import EmailValidator


class EmailValidatorAdapter(EmailValidator):
    def __init__(self, check_mx, skip_smtp):
        self.check_mx = check_mx
        self.skip_smtp = skip_smtp

    def is_valid(self, email: str) -> bool:
        return validate_email(email, check_mx=self.check_mx, skip_smtp=self.skip_smtp)
