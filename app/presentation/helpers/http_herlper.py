from ..protocols.http import Response


def bad_request(error: Exception) -> Response:
    return Response(status_code=400, body={"message": error})
