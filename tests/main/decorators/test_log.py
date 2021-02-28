from mock import patch, MagicMock

from app.presentation import Controller, HttpRequest, HttpResponse
from app.main import log_controller_handler
from app.presentation import ServerError, server_error


class FakeClass:
    def fake(self):
        ...


class ControllerStub(Controller):
    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            fake_class = FakeClass()
            fake_class.fake()
            return HttpResponse(status_code=200, body={"name": "John Doe"})
        except Exception:
            return server_error(error=ServerError(), traceback="Error on matrix")


def test_should_log_controller_decorator_return_http_response():
    controller_stub = ControllerStub()
    http_request = dict(
        body=dict(
            name="John",
            email="foo@example.com",
            password="password",
            password_confirmation="password",
        )
    )
    http_response = controller_stub.handle(http_request)
    assert http_response
    assert http_response.status_code == 200
    assert http_response.body == {"name": "John Doe"}


@patch("app.main.decorators.log.LogMongoRepo.log")
@patch.object(FakeClass, "fake")
def test_should_log_controller_decorator_call_log_error_repo_with_corret_value(
    mock_fake: MagicMock, mock_log: MagicMock
):
    mock_fake.side_effect = Exception()
    controller_stub = ControllerStub()
    http_request = dict(
        body=dict(
            name="John",
            email="foo@example.com",
            password="password",
            password_confirmation="password",
        )
    )
    controller_stub.handle(http_request)
    mock_log.assert_called_with("Error on matrix")
