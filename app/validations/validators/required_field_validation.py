from schema import Schema, SchemaError

from app.presentation import Validation, MissingParamError, InvalidParamError


class RequiredFieldValidation(Validation):
    def __init__(
        self,
        schema: Schema,
    ):
        self._schema = schema

    def validate(self, input):
        try:
            self._schema.validate(input)
        except SchemaError as se:
            error = se.code.split(":")
            if "Missing" in error[0]:
                return MissingParamError(error[1].strip())
            else:
                return InvalidParamError(error[1].strip())

    def __str__(self):
        return f"RequiredFieldValidation: {self.field_name}"
