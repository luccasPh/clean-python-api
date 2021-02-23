from ..protocols.http import Request, Response


class SignUpController:
    def handle(self, request: Request) -> Response:
        data = request.body
        if not data.get("name"):
            return Response(status_code=400, body={"message": "Missing param: name"})

        if not data.get("email"):
            return Response(status_code=400, body={"message": "Missing param: email"})
