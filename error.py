from enum import IntEnum

class HTTPStatus(IntEnum):
    OK = 200
    CREATED = 201
    FOUNd = 302
    BAD_REQUEST = 400
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_ERROR = 500

class ProtocolInterrupt(Exception):
    def __init__(self, *args: object) -> None:
        self.status = None
        self.msg = None
        self.location = None