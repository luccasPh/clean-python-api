class AccessDaniedError(Exception):
    def __init__(self):
        super().__init__("Access danied")
        self.name = "AccessDaniedError"
