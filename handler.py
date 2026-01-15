import urllib.parse
import uuid
import os
from http.server import BaseHTTPRequestHandler

# 1. 데이터 저장소
db = {}

class EssentialHandler(BaseHTTPRequestHandler):
    
    def _read_file(self, name):
        if not os.path.exists(name):
            return ""
        with open(name, 'r', encoding='utf-8') as f:
            return f.read()

    def _get_field(self, params, key):
        values = params.get(key)
        if values:
            return values[0].strip()
        else:
            return ""

    def _render_full_page(self):
        layout = self._read_file('index.html')
        
        if not db:
            content = self._read_file('empty.html')
        else:
            row = self._read_file('row.html')
            content = "".join(row.format(uid=u, task=i['task']) for u, i in db.items())

        return layout.replace('{rows}', content).encode('utf-8')

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self._render_full_page())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        params = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        
        id = self._get_field(params, 'id')
        task = self._get_field(params, 'task')

        if self.path == '/delete':
            db.pop(id, None)
        elif self.path == '/process':
            if id in db:
                db[id] = {'task': task}
            else:
                db[str(uuid.uuid4())] = {'task': task}

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()