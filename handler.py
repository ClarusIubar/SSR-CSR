from http.server import BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        message = "<h1>안녕하세요! 파이썬 서버입니다.</h1>"
        self.wfile.write(message.encode('utf-8'))
