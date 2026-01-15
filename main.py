from http.server import HTTPServer
from handler import MyHandler

host = 'localhost' # 내 컴퓨터
port = 8000        # 포트 번호
server = HTTPServer((host, port), MyHandler)

print(f"서버가 시작되었습니다. http://{host}:{port} 로 접속해보세요.")
print("종료하려면 터미널에서 Ctrl+C를 누르세요.")

if __name__ == "__main__":
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
        server.server_close()