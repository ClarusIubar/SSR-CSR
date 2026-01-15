import os, urllib.parse, uuid
from http.server import BaseHTTPRequestHandler

class EssentialHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, store):
        self.store = store
        super().__init__(request, client_address, server)

    def _read_file(self, name):
        if not os.path.exists(name): 
            return ""
        with open(name, "r", encoding='utf-8') as file: 
            return file.read()

    def _render(self, user_data):
        layout = self._read_file('html/index.html')
        rows = "".join(self._read_file('html/row.html').format(uid=u, task=i['task']) 
                       for u, i in user_data.items()) if user_data else self._read_file('html/empty.html')
        return layout.replace('{rows}', rows).encode('utf-8')

    def do_GET(self):
        if self.path == '/':
            sid, user_data, is_new = self.store.get_session(self.headers.get('Cookie'))
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            if is_new: 
                self.send_header('Set-Cookie', f'session_id={sid}; Path=/; HttpOnly')
            self.end_headers()
            self.wfile.write(self._render(user_data))

    def do_POST(self):
        _, user_data, _ = self.store.get_session(self.headers.get('Cookie'))
        size = int(self.headers.get('Content-Length', 0))
        data = urllib.parse.parse_qs(self.rfile.read(size).decode('utf-8'))
        
        uid, task = data.get('id', [''])[0], data.get('task', [''])[0]
        
        if self.path == '/delete':
            user_data.pop(uid, None)
        elif self.path == '/process':
            target_id = uid if uid in user_data else str(uuid.uuid4())
            user_data[target_id] = {'task': task}

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()