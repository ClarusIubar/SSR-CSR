from http.server import BaseHTTPRequestHandler      # 핸들러는 원래 필요했어.
from core import Request, Response                  # 이것도 내 집착이야.
from error import HTTPStatus, ProtocolInterrupt     # 에러도 따로 정했지.
from observer import Reconnaissance, Event, monitor # 관측시설이야.
import logic, json, urllib.parse                    # CRUD

# 아 몰라 이름은 가볍게.
class Handler(BaseHTTPRequestHandler):
    # [정찰 지침] IDE가 객체의 실체를 인지하도록 클래스 수준에서 선언 (조언 감사)
    req: Request
    res: Response

    # 선언적 라우팅: if-else로 나누는 거 너무 싫어요!
    @property
    def api_routes(self):
        return {
            ('GET',    '/api/tasks'): logic.perform_read,
            ('POST',   '/api/tasks'): logic.perform_create,
            ('PUT',    '/api/tasks'): logic.perform_update,
            ('DELETE', '/api/tasks'): logic.perform_delete,
        }

    @property
    def static_routes(self):
        return {
            '/': 'index.html',
            '/maslow': 'maslow.html',
            '/maslow.json': 'maslow.json'
        }

    def handle_request(self):
        with Reconnaissance(self) as recon:
            # 1. 시퀀스 객체 생성
            self.req, self.res = Request(), Response()
            self._fill_request() # core.py 규격에 맞게 매핑

            try:
                if self.path in self.static_routes:
                    self.serve_static_file(self.static_routes[self.path])
                else:
                    action = self.api_routes.get((self.command, self.path)) 
                    if not action: 
                        raise ProtocolInterrupt(HTTPStatus.NOT_FOUND)

                    # 관측: 로직 실행 시작
                    monitor.notify(Event.PROCESS, {"action": action.__name__}) # 실행하는 함수 이름이 보임.
                    
                    # req, res만 전달
                    action(self.req, self.res)

                self._emit(recon)

            except ProtocolInterrupt as pi: # 에러가 생기면
                self.res.status_code, self.res.body = pi.status, {"err": pi.status.name, "msg": pi.msg}
                self._emit(recon)

    def _fill_request(self):
        """core.py의 Request 규격에 맞춰 Raw 데이터를 객체화"""
        self.req.method = self.command
        self.req.path = self.path
        self.req.protocol = self.protocol_version
        
        self.req.content_type = self.headers.get('Content-Type', '')
        self.req.user_agent = self.headers.get('User-Agent', '')

        for key, value in self.headers.items():
            self.req.headers[key] = value

        # [핵심 개선] Body 파싱 통합: logic.py에서 handler.rfile을 직접 읽는 중복을 제거
        length = int(self.headers.get('Content-Length', 0))
        if length > 0:
            raw = self.rfile.read(length).decode('utf-8')
            if 'application/json' in self.req.content_type:
                self.req.body = json.loads(raw)
            else:
                self.req.body = dict(urllib.parse.parse_qsl(raw))
        else:
            self.req.body = {}

    def _emit(self, recon):
        """core.py의 Response 규격을 Raw 프로토콜로 변환하여 방출"""
        reason = self.res.reason_phrase or "OK"
        status_obj = self.res.status_code or HTTPStatus.OK
        status_val = status_obj.value
        status_name = status_obj.name
        
        monitor.notify(Event.EMIT, {"status": status_name})
        logs = recon.browser_obs.flush()
        
        self.send_response(status_val, reason) 
        for key, value in self.res.header.items(): 
            self.send_header(key, value)
        self.send_header('X-Sequence-Trace', logs) # 이제 EMIT이 포함된 logs가 방출됨
        self.end_headers()
        
        # Body 방출
        if self.res.body:
            if isinstance(self.res.body, (dict, list)): 
                self.wfile.write(json.dumps(self.res.body).encode('utf-8'))
            else: 
                self.wfile.write(self.res.body)

    def _get_content_type(self, filename):
        content_types = {
            'html': 'text/html; charset=utf-8',
            'css': 'text/css; charset=utf-8',
            'json': 'application/json; charset=utf-8',
        }
        ext = filename.split('.')[-1] # 확장자
        return content_types.get(ext, 'text/plain')

    def serve_static_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                content = f.read()
                # res 객체에 위임하여 _emit에서 처리하도록 유도
                self.res.body = content
                self.res.header['Content-Type'] = self._get_content_type(filename)
                
                # 정적 파일 관측 시점 기록
                monitor.notify(Event.EMIT, {"static_file": filename, "size": len(content)})
        except FileNotFoundError:
            raise ProtocolInterrupt(HTTPStatus.NOT_FOUND, f"Missing: {filename}")

    # 지원할 메서드 확장
    def do_GET(self):    self.handle_request()
    def do_POST(self):   self.handle_request()
    def do_PUT(self):    self.handle_request()
    def do_DELETE(self): self.handle_request()