
class GeneralException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UnimplementedMethodException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class BadFieldValueException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
