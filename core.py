from error import HTTPStatus # 기본값 설정을 위해 임포트
from typing import Any # 어떤 타입이든 허용하기 위해 필요 # 와 진짜 양아치다. # 내가 이걸 쓴다고? ㅋㅋ

class Request:
    def __init__(self):
        # request-line
        self.method = ""
        self.path = ""
        self.protocol = "HTTP/1.1" # protocol

        # request-header
        # self.host = None
        # self.auth = None

        # headers
        self.headers = {}
        self.content_type = "" # 봉인해제!
        self.user_agent = ""   # 봉인해제!

        # body
        self.body: Any = None

class Response:
    def __init__(self):
        # response-line
        self.protocol = "HTTP/1.1" # protocol
        self.status_code = HTTPStatus.OK # None 대신 기본값 주입
        self.reason_phrase = "OK"

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
        self.body: Any = None # pylance에러 때문에 일단 어쩔 수 없이.
