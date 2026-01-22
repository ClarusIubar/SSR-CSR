from http.server import BaseHTTPRequestHandler      # 핸들러는 원래 필요했어.
from core import Request, Response                  # 이것도 내 집착이야.
from error import HTTPStatus, ProtocolInterrupt     # 에러도 따로 정했지.
from observer import Reconnaissance, Event, monitor # 관측시설이야.
import logic, json                                  # CRUD

# 아 몰라 이름은 가볍게.
class Handler(BaseHTTPRequestHandler):
    # [정찰 지침] IDE가 객체의 실체를 인지하도록 클래스 수준에서 선언
    req: Request
    res: Response

    def handle_request(self):
        with Reconnaissance(self) as recon:
            # 1. 시퀀스 객체 생성
            self.req, self.res = Request(), Response()
            self._fill_request() # core.py 규격에 맞게 매핑

            # self.req = Request(self)
            # self.res = Response(self)
            # self.monitor = None # 모니터 필요하겠지. 동작할 때 마다 보고하게 시킬거니까.
            
            # 할 수도 있고, 안 쓸 수도 있고 일단 주석처리해.
            # router = {
            #     ('GET' , '/client' ):    NotImplemented,
            #     ('GET' , '/api/tasks' ): NotImplemented,
            #     ('POST', '/api/tasks' ): NotImplemented,
            #     ('POST', '/api/delete'): NotImplemented
            # }

            try:
                static_routes = {
                    '/': 'index.html',
                    '/maslow': 'maslow.html',
                    '/maslow.json': 'maslow.json'
                }

                if self.path in static_routes:
                    # 모든 정적 파일은 이제 이 메서드 하나로 통합니다.
                    self.serve_static_file(static_routes[self.path])
                    return
                
                # 2. 라우팅 테이블 정의
                router = {
                    ('GET', '/api/tasks'):  logic.perform_read,
                    ('POST', '/api/tasks'): logic.perform_create
                }
                
                # 4. 행위 식별 및 집행
                action = router.get((self.command, self.path)) # method, path 아, request-line 애들이구나.
                if not action: # 못찾겠다 꾀꼬리
                    raise ProtocolInterrupt(HTTPStatus.NOT_FOUND)
                    
                # 관측: 로직 실행 시작
                monitor.notify(Event.PROCESS, {"action": action.__name__})
                action(self, self.req, self.res)

                # 5. 정상 응답 방출
                self._emit(recon.browser_obs.flush())

            except ProtocolInterrupt as pi: # 에러가 생기면
                # pi.status는 Enum 객체이므로 직접 대입
                self.res.status_code, self.res.body = pi.status, {"err": pi.status.name}
                self._emit(recon.browser_obs.flush())

    def _fill_request(self):
        """core.py의 Request 규격에 맞춰 Raw 데이터를 객체화"""
        # [해결] 클래스 상단 선언을 통해 self.req.method의 빨간 줄 제거
        self.req.method = self.command
        self.req.path = self.path
        self.req.protocol = self.protocol_version
        
        # [중요] logic.py의 AttributeError 방지를 위해 명시적 매핑 추가
        self.req.content_type = self.headers.get('Content-Type', '')
        self.req.user_agent = self.headers.get('User-Agent', '')

        # core.py의 Request는 'headers'(복수형)를 소유함
        for key, value in self.headers.items():
            self.req.headers[key] = value

    def _emit(self, logs):
        """core.py의 Response 규격을 Raw 프로토콜로 변환하여 방출"""
        # Status-Line 구성: 사유 구절이 없을 경우 "OK"로 대체
        reason = self.res.reason_phrase or "OK"
        
        # status_code가 설정되지 않았을 경우 기본값 OK(200) 적용
        status_obj = self.res.status_code or HTTPStatus.OK
        status_val = status_obj.value
        status_name = status_obj.name
        
        # send_response, send_header, end_headers 세트메뉴 123
        self.send_response(status_val, reason) #status, reason_phrase
        for key, value in self.res.header.items(): # Response는 'header' 단수형
            self.send_header(key, value)
        self.send_header('X-Sequence-Trace', logs) # 관측 데이터 전파
        self.end_headers()
        
        # Body 방출
        if self.res.body:
            self.wfile.write(json.dumps(self.res.body).encode('utf-8'))
        
        # 최종 관측 보고
        monitor.notify(Event.EMIT, {"status": status_name})

    def serve_index(self):
        """인덱스 페이지 서빙"""
        try:
            with open('index.html', 'rb') as f:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            # 예외 발생 시 에러 시퀀스로 강제 전이
            raise ProtocolInterrupt(HTTPStatus.NOT_FOUND, "Index missing")
        

    def serve_static_file(self, filename):
            content_types = {
                'html': 'text/html; charset=utf-8',
                'css': 'text/css; charset=utf-8',
                'json': 'application/json; charset=utf-8',
            }
            ext = filename.split('.')[-1] # .뒤에 끝에는 확장자
            content_type = content_types.get(ext, 'text/plain') # 없으면 그냥 text로 처리

            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                    monitor.notify(Event.EMIT, {"static_file": filename, "size": len(content)})
                    
                    self.send_response(HTTPStatus.OK)
                    self.send_header('Content-Type', content_type) # * 이렇게 할 거면, 애초에 확장자만 다루는 것을 함수화하면 되지 않나?
                    self.end_headers()
                    self.wfile.write(content)
                    
            except FileNotFoundError:
                raise ProtocolInterrupt(HTTPStatus.NOT_FOUND, f"Missing: {filename}")

    # 오버라이딩 빡세게 안할 거임. 만든 거 호출해버리면 그만이겠지.
    def do_GET(self):  self.handle_request()
    def do_POST(self): self.handle_request()
