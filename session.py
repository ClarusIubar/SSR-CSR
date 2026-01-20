import uuid
import urllib.parse

class SessionStore:
    def __init__(self):
        self._storage = {}

    def get_session(self, cookie):
        cookies = urllib.parse.parse_qs((cookie or "").replace('; ', '&'))
        sid = cookies.get('session_id', [None])[0]

        is_new = False
        if not sid or sid not in self._storage:
            sid = str(uuid.uuid4())
            self._storage[sid] = {}
            is_new = True
        
        return sid, self._storage[sid], is_new