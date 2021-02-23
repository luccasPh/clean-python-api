class SignUpController:
    def handle(self, request: dict):
        data = request.get("body")
        if not data.get("name"):
            return {"status_code": 400, "message": "Missing param: name"}

        if not data.get("email"):
            return {"status_code": 400, "message": "Missing param: email"}
