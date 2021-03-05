from app.presentation import Validation, UniqueValueError
from ..protocols.db_search_by_field import DbSearchByField


class UniqueFieldValidation(Validation):
    def __init__(
        self,
        field_name: str,
        db_search_by_field: DbSearchByField,
    ):
        self.field_name = field_name
        self._db_search_by_field = db_search_by_field

    def validate(self, input):
        result = self._db_search_by_field.search_by_field(
            self.field_name, input[self.field_name]
        )
        if result:
            return UniqueValueError(self.field_name)

    def __str__(self):
        return f"UniqueFieldValidation: {self.field_name}"
