
class GeneralException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message)


class UnimplementedMethodException(GeneralException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BadFieldValueException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ClientAndServerOutOfSyncException(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)