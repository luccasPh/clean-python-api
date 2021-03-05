from app.presentation import Validation, MissingParamError


class RequiredFieldValidation(Validation):
    def __init__(
        self,
        field_name: str,
    ):
        self.field_name = field_name

    def validate(self, input):
        if self.field_name not in input:
            return MissingParamError(self.field_name)

    def __str__(self):
        return f"RequiredFieldValidation: {self.field_name}"
