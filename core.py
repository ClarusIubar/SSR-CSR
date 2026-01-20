import urllib.parse, uuid, json

class Request:
    def __init__(self, handler):
        self.method = handler.command
        self.path = handler.path.split('?')[0].rstrip('/') or '/'
        self.cookie = handler.headers.get('Cookie', '')
        self._handler = handler

    # 메서드로 쓰기 싫어. req.call으로 쓸래.
    @property
    def call(self):
        return (self.method, self.path)

    # req.get_form_data()같이 메서드로 쓰기 싫어.
    # req.form으로 쓸래.
    @property
    def form(self):
        # 1. 헤더에서 읽어야 할 길이를 먼저 확보
        content_length = self._handler.headers.get('Content-Length')
        if not content_length or int(content_length) <= 0:
            return {}
            
        # 2. 지정된 바이트(int)만큼만 정확히 읽어서 소켓 대기를 해제
        try:
            size = int(content_length)
            raw_body = self._handler.rfile.read(size).decode('utf-8')
            # 3. 파싱 후 첫 번째 값만 취해 딕셔너리화
            parsed = urllib.parse.parse_qs(raw_body)
            return {k: v[0].strip() for k, v in parsed.items()}
        except Exception:
            return {}

    def new_id(self):
        return str(uuid.uuid4())

class Response:
    def __init__(self, handler):
        self._handler = handler

    def html(self, body, sid=None):
        self._handler.send_response(200)
        self._handler.send_header('Content-type', 'text/html; charset=utf-8')
        if sid: self._handler.send_header('Set-Cookie', f'session_id={sid}; Path=/; HttpOnly')
        self._handler.end_headers()
        self._handler.wfile.write(body.encode('utf-8'))

    def redirect(self, location):
        self._handler.send_response(303)
        self._handler.send_header('Location', location)
        self._handler.end_headers()

    def error(self, code, message):
        self._handler.send_error(code, message)

    # CSR -> 데이터만 이동
    def json(self, data, sid=None):
        try:
            body = json.dumps(data, ensure_ascii=False)
            self._handler.send_response(200)
            self._handler.send_header('Content-type', 'application/json; charset=utf-8')
            if sid: self._handler.send_header('Set-Cookie', f'session_id={sid}; Path=/; HttpOnly')
            self._handler.end_headers()
            self._handler.wfile.write(body.encode('utf-8'))
        except (ConnectionAbortedError, BrokenPipeError):
            # 브라우저가 도망갔을 경우, 무리하게 보내지 않고 조용히 행위를 종료함
            print("클라이언트가 응답을 기다리지 않고 연결을 끊었습니다.")