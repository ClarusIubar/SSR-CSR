from http.server import BaseHTTPRequestHandler
from core import Request, Response
from renderer import ViewRenderer
from services import MaslowService

class EssentialHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, store, base_dir):
        self.store = store
        self.base_dir = base_dir
        super().__init__(request, client_address, server)

    def handle_request(self):
        # 1. 독립 자원 할당
        self.req = Request(self)
        self.res = Response(self)
        self.view = ViewRenderer(self.base_dir)
        self.service = MaslowService(self.base_dir)
        
        # 2. 경로 지도
        router = {
            # 1. 기존 SSR 경로
            ('GET' , '/'       ): self.show_index,
            ('GET' , '/maslow' ): self.show_maslow,
            ('POST', '/process'): self.handle_save,
            ('POST', '/delete' ): self.handle_remove,
            # 2. 별도의 API 경로
            ('GET' , '/client' ): self.show_client_page,
            ('GET' , '/api/tasks' ): self.api_get_tasks,
            ('POST', '/api/tasks' ): self.api_save_task,
            ('POST', '/api/delete'): self.api_delete_task
        }
        
        # 3. 실행: 예외 없이 즉각 대응
        action = router.get(self.req.call, self.not_found)
        action()

    # 경로의 함수를 실행해
    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()

    # SSR 용도
    def show_index(self):
        session = self.store.get_session(self.req.cookie)
        self.res.html(self.view.render_index(session['data']), 
                      session['sid'] if session['is_new'] else None)

    def show_maslow(self):
        session = self.store.get_session(self.req.cookie)
        self.res.html(self.view.render_maslow(self.service.get_steps()), 
                      session['sid'] if session['is_new'] else None)

    def handle_save(self):
        self._execute_save()
        self.res.redirect('/')

    def handle_remove(self):
        self._execute_delete()
        self.res.redirect('/')

    # CSR용도
    def show_client_page(self):
        self.res.html(self.view._read('client_page'))

    def api_get_tasks(self):
        session = self.store.get_session(self.req.cookie)
        self.res.json(session['data']) 

    def api_save_task(self):
        _, uid = self._execute_save()
        self.res.json({"status": "success", "id": uid})

    def api_delete_task(self):
        _, existed = self._execute_delete()
        self.res.json({"status": "success" if existed else "fail"})

    # 공통
    def not_found(self):
        self.res.error(404, f"Path '{self.req.path}' is invalid.")

    # logic만 분리해보기
    def _execute_save(self):
        # 공통로직 추출
        session = self.store.get_session(self.req.cookie)
        user_data = session['data']
        form = self.req.form
        uid = form.get('id') or self.req.new_id()
        user_data[uid] = {'task': form.get('task', '')}
        return session, uid
    
    def _execute_delete(self):
        session = self.store.get_session(self.req.cookie)
        uid = self.req.form.get('id')

        existed = uid in session['data']
        if existed:
            session['data'].pop(uid)

        return session, existed