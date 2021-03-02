import pytest
import mongomock
from mock import patch, MagicMock

from app.domain import AccountModel, AddAccount, AddAccountModel
from app.presentation import (
    SignUpController,
    HttpRequest,
    Validation,
    MissingParamError,
)


class AddAccountStub(AddAccount):
    def add(self, data: AddAccountModel) -> AccountModel:
        fake_account = {
            "id": "valid_id",
            "name": "valid_name",
            "email": "valid_email@example.com",
            "hashed_password": "valid_password_hash",
        }
        return AccountModel(**fake_account)


class ValidationStub(Validation):
    def validate(self, input):
        ...


@pytest.fixture
def sut():
    add_account_stub = AddAccountStub()
    validation_stub = ValidationStub()
    sut = SignUpController(add_account_stub, validation_stub)
    yield sut


@patch.object(AddAccountStub, "add")
def test_should_call_add_account_correct_values(
    mock_add: MagicMock, sut: SignUpController
):
    mock_add.return_value = AccountModel(
        id="valid_id",
        name="valid_name",
        email="valid_email@example.com",
        hashed_password="valid_password_hash",
    )

    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    sut.handle(request)
    expected = AddAccountModel(
        name="John Doe",
        email="test@example.com",
        password="test",
    )
    mock_add.assert_called_with(expected)


@patch("app.main.decorators.log.get_collection")
@patch.object(AddAccountStub, "add")
def test_should_500_if_add_account_raise_exception(
    mock_add: MagicMock, mock_get_collection: MagicMock, sut: SignUpController
):
    mock_add.side_effect = Exception("Error on matrix")
    mock_get_collection.return_value = mongomock.MongoClient().db.collection
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 500
    assert response.body["message"] == "Internal server error"


def test_should_200_if_data_is_valid(sut: SignUpController):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    expected = {
        "id": "valid_id",
        "name": "valid_name",
        "email": "valid_email@example.com",
        "hashed_password": "valid_password_hash",
    }
    response = sut.handle(request)
    assert response.status_code == 200
    assert response.body == expected


@patch.object(ValidationStub, "validate")
def test_should_call_validation_correct_value(
    mock_validate: MagicMock, sut: SignUpController
):
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    sut.handle(request)
    mock_validate.assert_called_with(request.body)


@patch.object(ValidationStub, "validate")
def test_should_400_if_validation_returns_error(
    mock_validate: MagicMock, sut: SignUpController
):
    mock_validate.return_value = MissingParamError("any_field")
    request = HttpRequest(
        body={
            "name": "John Doe",
            "email": "test@example.com",
            "password": "test",
            "password_confirmation": "test",
        }
    )
    response = sut.handle(request)
    assert response.status_code == 400
    assert response.body == dict(message="Missing param: any_field")
