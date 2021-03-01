from .validation import Validation


class ValidationComposite(Validation):
    def __init__(self, validations: list[Validation]):
        self.validations = validations

    def validate(self, input):
        for validation in self.validations:
            is_error = validation.validate(input)
            if is_error:
                return is_error
