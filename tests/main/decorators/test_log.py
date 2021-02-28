from app.presentation import Controller, HttpRequest, HttpResponse
from app.main import log_controller_handler


class ControllerStub(Controller):
    @log_controller_handler
    def handle(self, request: HttpRequest) -> HttpResponse:
        http_response = dict(status_code=200, body={"name": "John Doe"})
        return http_response


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
    assert http_response["status_code"] == 200
    assert http_response["body"] == {"name": "John Doe"}
