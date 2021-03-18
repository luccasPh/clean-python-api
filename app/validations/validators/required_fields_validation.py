from schema import Schema, SchemaError

from app.presentation import Validation, MissingParamError, InvalidParamError


class RequiredFieldsValidation(Validation):
    def __init__(self, schema: Schema, name: str):
        self._schema = schema
        self._name = name

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
        return f"RequiredFieldValidation: {self._name}"
