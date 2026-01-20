import os, urllib.parse, uuid, json
from http.server import BaseHTTPRequestHandler

class EssentialHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, store):
        self.store = store
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(request, client_address, server)

    def _read_file(self, name):
        clean_name = name.replace('html/', '')
        path = os.path.join(self.base_dir, 'html', clean_name)
        
        if not os.path.exists(path): 
            print(f"\n[ERROR] 파일이 어디에 있나요: {path}")
            return ""
            
        with open(path, "r", encoding='utf-8') as file: 
            return file.read()

    def _render(self, user_data):
        layout = self._read_file('index.html')
        row = self._read_file('row.html')
        empty = self._read_file('empty.html')
        rows = "".join(row.format(uid=u, task=i['task']) 
                       for u, i in user_data.items()) if user_data else empty
        
        return layout.replace('{rows}', rows).encode('utf-8')

    def do_GET(self):
        # 도대체 왜 이래야 하나
        clean_path = self.path.split('?')[0].rstrip('/')
        if clean_path == '': clean_path = '/'

        router = {
            '/': self.route_index,
            '/maslow': self.route_maslow
        }

        action = router.get(clean_path)
        if action:
            action()
        else: # 주소창의 아이콘 따위
            if clean_path == '/favicon.ico': return
            self.send_error(404, f"Path Not Found: {self.path}")

    def route_index(self):
        sid, user_data, is_new = self.store.get_session(self.headers.get('Cookie'))
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        if is_new: 
            self.send_header('Set-Cookie', f'session_id={sid}; Path=/; HttpOnly')
        self.end_headers()
        self.wfile.write(self._render(user_data))

    def route_maslow(self):
        # 데이터 폴더도 절대 경로로 지정
        json_path = os.path.join(self.base_dir, 'data', 'maslow.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                maslow_steps = json.load(f)
        else:
            maslow_steps = []

        brick = self._read_file('maslow_brick.html')
        stack = "".join(brick.format(**step) for step in maslow_steps)
        layout = self._read_file('maslow.html')
        content = layout.replace('{stack}', stack).encode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        user_data = self.store.get_session(self.headers.get('Cookie'))[1]
        size = int(self.headers.get('Content-Length', 0))
        data = urllib.parse.parse_qs(self.rfile.read(size).decode('utf-8'))
        
        uid = data.get('id', [''])[0].strip()
        task = data.get('task', [''])[0].strip()
        
        if self.path == '/delete':
            user_data.pop(uid, None)
        elif self.path == '/process':
            target_id = uid if uid in user_data else str(uuid.uuid4())
            user_data[target_id] = {'task': task}

        # 새로고침시 리다이렉션
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()