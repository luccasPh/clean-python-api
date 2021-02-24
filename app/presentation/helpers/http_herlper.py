from ..protocols.http import Response


def bad_request(error: Exception) -> Response:
    return Response(status_code=400, body={"message": error})


def server_error(error: Exception) -> Response:
    return Response(status_code=500, body={"message": error})


def ok(data) -> Response:
    return Response(status_code=200, body=data)
