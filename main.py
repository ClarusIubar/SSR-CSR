from http.server import HTTPServer
from handler import EssentialHandler

HOST = 'localhost'
PORT = 8000

if __name__ == "__main__":
    # 핸들러를 외부 모듈에서 가져와 서버를 가동합니다.
    server = HTTPServer((HOST, PORT), EssentialHandler)
    print(f"서버 시스템 기동 중: http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버 종료 신호를 수신했습니다.")
        server.server_close()