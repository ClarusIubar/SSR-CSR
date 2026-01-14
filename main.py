from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. 요청을 처리할 핸들러 클래스 정의
class MyRequestHandler(BaseHTTPRequestHandler):
    
    # GET 요청이 들어오면 실행되는 함수
    def do_GET(self):
        # [응답 준비 1] 상태 코드 전송 (200 = 성공)
        self.send_response(200)
        
        # [응답 준비 2] 헤더 전송 (내용이 텍스트/HTML임을 알림)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # [응답 본문] 실제 보여줄 내용 (반드시 바이트 형태로 인코딩 필요)
        message = "<h1>안녕하세요! 파이썬 서버입니다.</h1>"
        self.wfile.write(message.encode('utf-8'))

# 2. 서버 설정 (주소와 포트 지정)
host = 'localhost' # 내 컴퓨터
port = 8000        # 포트 번호

# 3. 서버 실행 인스턴스 생성
server = HTTPServer((host, port), MyRequestHandler)

print(f"서버가 시작되었습니다. http://{host}:{port} 로 접속해보세요.")
print("종료하려면 터미널에서 Ctrl+C를 누르세요.")

# 4. 서버 무한 대기 (요청이 올 때까지 계속 실행)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
    server.server_close()