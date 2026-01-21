import urllib.parse, uuid, json

class Request:
    def __init__(self, handler):
        self.method = handler.command
        self.path = handler.path.split('?')[0].rstrip('/') or '/'
        self._handler = handler

    @property
    def call(self):
        return (self.method, self.path)

    def new_id(self):
        return str(uuid.uuid4())

# 서버에서 요청을 받는 것만 생각해서 @property를 쉽게 생각했는데,
# 클라이언트가 응답을 받는 것은 JSON이나 데이터를 받아야 하는데,
# 왜 여기는 미처 @property를 쓸 생각을 미쳐 못했나.
# 서버측면에서만 생각했나봄.
class Response:
    def __init__(self, handler):
        self._handler = handler

    def json(self, data, sid=None):
        try:
            body = json.dumps(data, ensure_ascii=False)
            self._handler.send_response(200)
            self._handler.send_header('Content-type', 'application/json; charset=utf-8')
            if sid: self._handler.send_header('Set-Cookie', f'session_id={sid}; Path=/; HttpOnly')
            self._handler.end_headers()
            self._handler.wfile.write(body.encode('utf-8'))
        except (ConnectionAbortedError, BrokenPipeError):
            print("클라이언트가 응답을 기다리지 않고 연결을 끊었습니다.")