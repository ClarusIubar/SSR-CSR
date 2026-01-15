from http.server import ThreadingHTTPServer
from handler import EssentialHandler
from session import SessionStore
from functools import partial

HOST, PORT = 'localhost', 8000

if __name__ == "__main__":
    store = SessionStore()
    handler_factory = partial(EssentialHandler, store=store)
    server = ThreadingHTTPServer((HOST, PORT), handler_factory)
    
    print(f"병렬 세션 시스템 기동: http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n자원 정리 및 종료")
        server.server_close()