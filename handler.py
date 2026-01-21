from http.server import BaseHTTPRequestHandler
from core import Request, Response

class EssentialHandler(BaseHTTPRequestHandler):

    def handle_request(self):
        self.req = Request(self)
        self.res = Response(self)
        
        router = {
            ('GET' , '/client' ): self.show_client_page,
            ('GET' , '/api/tasks' ): self.api_get_tasks,
            ('POST', '/api/tasks' ): self.api_save_task,
            ('POST', '/api/delete'): self.api_delete_task
        }
        
        # 3. 실행: 예외 없이 즉각 대응
        action = router.get(self.req.call)
        # action()

    # 경로의 함수를 실행해
    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()

    # CSR용도
    def show_client_page(self):
        pass

    def api_get_tasks(self):
        pass

    def api_save_task(self):
        pass

    def api_delete_task(self):
        pass