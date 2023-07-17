
class GeneralException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message)


class UnimplementedMethodException(GeneralException):
    def __init__(self, *args):
        super().__init__(*args)


class BadFieldValueException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class BadFieldTypeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ClientAndServerOutOfSyncException(RuntimeError):
    def __init__(self, *args):
        super().__init__(*args)


class CollectionNotChosenYetException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class DatabaseNotSelectedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class EmptyCollectionException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class FieldNameAlreadyInUseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
