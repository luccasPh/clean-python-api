from app.controllers.signup import SignUpController


def test_should_400_if_no_name_provided():
    sut = SignUpController()
    request = {
        "body": {
            "email": "test@example.com",
            "password": "teste",
            "password_confirmation": "test",
        }
    }
    response = sut.handle(request)
    assert response["status_code"] == 400
    assert response["message"] == "Missing param: name"


def test_should_400_if_no_email_provided():
    sut = SignUpController()
    request = {
        "body": {
            "name": "John Doe",
            "password": "teste",
            "password_confirmation": "test",
        }
    }
    response = sut.handle(request)
    assert response["status_code"] == 400
    assert response["message"] == "Missing param: email"
