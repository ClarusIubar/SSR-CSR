from http.server import HTTPServer
from handler import EssentialHandler
from session import SessionStore
from functools import partial

if __name__ == "__main__":
    store = SessionStore()
    handler_factory = partial(EssentialHandler, store=store)
    server = HTTPServer(('localhost', 8000), handler_factory)
    server.serve_forever()