class SignUpController:
    def handle(self, request):
        return {"status_code": 400, "message": "Missing param: name"}
