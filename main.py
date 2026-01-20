import os
from http.server import ThreadingHTTPServer
from handler import EssentialHandler
from session import SessionStore
from functools import partial

HOST, PORT = 'localhost', 8000

if __name__ == "__main__":
    store = SessionStore()
    base_path = os.path.dirname(os.path.abspath(__file__))

    handler_factory = partial(EssentialHandler, store=store, base_dir=base_path)
    server = ThreadingHTTPServer((HOST, PORT), handler_factory)
    
    print(f"서버 기동: http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n종료")
        server.server_close()