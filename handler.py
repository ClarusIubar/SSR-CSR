import urllib.parse
import uuid
import os
from http.server import BaseHTTPRequestHandler

db = {}

class EssentialHandler(BaseHTTPRequestHandler):

    def _read_file(self, name):
        if not os.path.exists(name):
            return ""
        with open(name, "r", encoding='utf-8') as file:
            return file.read()
    
    def _get_field(self, data, key):
        value = data.get(key)
        if value:
            return value[0].strip()
        return ""
    
    def _render(self):
        layout = self._read_file('index.html')

        if not db:
            rows = self._read_file('empty.html')
        else:
            row = self._read_file('row.html')
            rows = "".join(row.format(uid=u, task=i['task']) for u, i in db.items())

        return layout.replace('{rows}', rows).encode('utf-8')
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self._render())

    def do_POST(self):
        size = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(size).decode('utf-8')

        data = urllib.parse.parse_qs(body)

        uid = self._get_field(data, 'id')
        task = self._get_field(data, 'task')

        if self.path == '/delete':
            db.pop(uid, None)

        elif self.path == '/process':
            if uid in db:
                db[uid] = {'task' : task}
            else:
                db[str(uuid.uuid4())] = {'task' : task}

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()