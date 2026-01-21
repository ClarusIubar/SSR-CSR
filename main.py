import os
from http.server import HTTPServer
from handler import EssentialHandler

HOST, PORT = 'localhost', 8000

if __name__ == "__main__":

    base_path = os.path.dirname(os.path.abspath(__file__))
    server = HTTPServer((HOST, PORT), EssentialHandler)
    
    print(f"서버 기동: http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n종료")
        server.server_close()