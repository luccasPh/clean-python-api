class UniqueValueError(Exception):
    def __init__(self, param_name):
        super().__init__(f"The received {param_name} is already in use: ")
        self.name = "UniqueValueError"
