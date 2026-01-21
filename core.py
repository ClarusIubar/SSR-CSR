class Request:
    def __init__(self):
        # request-line
        self.method = None
        self.path = None
        self.protocol = "HTTP/1.1" # protocol

        # request-header
        # self.host = None
        # self.auth = None
        # self.content_type = None
        # self.user_agent = None

        # headers
        self.headers = {} # 너무 세분화 했나?

        # body
        self.body = None

class Response:

    def __init__(self):
        # response-line
        self.protocol = "HTTP/1.1" # protocol
        self.status_code = None
        self.reason_phrase = None

        # response-header
        # self.content_type = "application/json; charset=utf-8" # json
        # self.set_cookie = None
        # self.cache_control = None
        # self.server = None

        # headers
        self.header = {
            "Content-Type" : "application/json; charset=utf-8",
            "Server": "PurePythonServer/1.0"
        }

        # body
        self.body = None
