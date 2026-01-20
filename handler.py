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
            ('GET' , '/'       ): self.show_index,
            ('GET' , '/maslow' ): self.show_maslow,
            ('POST', '/process'): self.handle_save,
            ('POST', '/delete' ): self.handle_remove
        }
        
        # 3. 실행: 예외 없이 즉각 대응
        action = router.get(self.req.call, self.not_found)
        action()

    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()
    def show_index(self):
        session = self.store.get_session(self.req.cookie)
        self.res.html(self.view.render_index(session['data']), 
                      session['sid'] if session['is_new'] else None)

    def show_maslow(self):
        session = self.store.get_session(self.req.cookie)
        self.res.html(self.view.render_maslow(self.service.get_steps()), 
                      session['sid'] if session['is_new'] else None)

    def handle_save(self):
        session = self.store.get_session(self.req.cookie)
        user_data = session['data']
        form = self.req.form
        uid = form.get('id') or self.req.new_id()
        user_data[uid] = {'task': form.get('task', '내용 없음')}
        self.res.redirect('/')

    def handle_remove(self):
        session = self.store.get_session(self.req.cookie)
        session['data'].pop(self.req.form.get('id'), None)
        self.res.redirect('/')

    def not_found(self):
        self.res.error(404, f"Path '{self.req.path}' is invalid.")