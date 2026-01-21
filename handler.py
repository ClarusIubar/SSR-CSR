from http.server import BaseHTTPRequestHandler
from core import Request, Response

# 아 몰라 이름은 가볍게.
class Handler(BaseHTTPRequestHandler):

    def handle_request(self):
        self.req = Request(self)
        self.res = Response(self)
        self.monitor = None # 모니터 필요하겠지. 동작할 때 마다 보고하게 시킬거니까.
        
        # 할 수도 있고, 안 쓸 수도 있고 일단 주석처리해.
        # router = {
        #     ('GET' , '/client' ):    NotImplemented,
        #     ('GET' , '/api/tasks' ): NotImplemented,
        #     ('POST', '/api/tasks' ): NotImplemented,
        #     ('POST', '/api/delete'): NotImplemented
        # }

    # 오버라이딩 빡세게 안할 거임. 만든 거 호출해버리면 그만이겠지.
    def do_GET(self):  self.handle_request()
    def do_POST(self): self.handle_request()