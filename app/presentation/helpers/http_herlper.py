from ..protocols.http import HttpResponse


def bad_request(error: Exception) -> HttpResponse:
    return HttpResponse(status_code=400, body={"message": error.args[0]})


def server_error(error: Exception, traceback: str) -> HttpResponse:
    return HttpResponse(
        status_code=500, body={"message": error.args[0], "traceback": traceback}
    )


def ok(data) -> HttpResponse:
    return HttpResponse(status_code=200, body=data)
