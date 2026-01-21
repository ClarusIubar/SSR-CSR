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
    def __init__(self, status: HTTPStatus, msg: str = ''):
        self.status = status
        self.msg = msg
        # self.location = None