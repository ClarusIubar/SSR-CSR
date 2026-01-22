import os, sys
from http.server import HTTPServer
from handler import Handler

HOST, PORT = 'localhost', 8000

if __name__ == "__main__":

    base_path = os.path.dirname(os.path.abspath(__file__))
    server = HTTPServer((HOST, PORT), Handler)
    
    print(f"서버 기동: http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n종료")
        server.server_close()
        sys.exit(0) # 정찰자를 넣어서 나의 신호가 씹히나보다.
        # 그렇다고 거기를 또 손대면 안됨.