from http.server import ThreadingHTTPServer
from handler import EssentialHandler
from session import SessionStore
from functools import partial

HOST, PORT = 'localhost', 8000

if __name__ == "__main__":
    store = SessionStore()
    handler_factory = partial(EssentialHandler, store=store)
    server = ThreadingHTTPServer((HOST, PORT), handler_factory)
    
    print(f"서버 기동: http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n종료")
        server.server_close()