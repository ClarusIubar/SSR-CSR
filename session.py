import uuid
import urllib.parse

class SessionStore:
    def __init__(self):
        self._storage = {}

    def get_session(self, cookie):
            # 쿠키에서 값 파싱하는 거 나는 모르지만, AI가 알려줌.
            cookies = urllib.parse.parse_qs((cookie or "").replace('; ', '&'))  
            sid = cookies.get('session_id', [None])[0]
            is_new = False 
            
            if not sid or sid not in self._storage:
                sid = str(uuid.uuid4())
                self._storage[sid] = {}
                is_new = True
            
            # 튜플의 나열이 아닌, 명확한 이름을 가진 사전형으로 반환
            return {
                'sid': sid,
                'data': self._storage[sid],
                'is_new': is_new
            }