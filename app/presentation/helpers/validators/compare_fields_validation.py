from ...protocols.validation import Validation
from ...errors.invalid_param_error import InvalidParamError


class CompareFieldsValidation(Validation):
    def __init__(self, field_name: str, field_to_compare_name: str):
        self.field_name = field_name
        self.field_to_compare_name = field_to_compare_name

    def validate(self, input):
        if input[self.field_name] != input[self.field_to_compare_name]:
            return InvalidParamError(self.field_to_compare_name)

    def __str__(self):
        return f"CompareFieldsValidation: {self.field_name} -> {self.field_to_compare_name}"
