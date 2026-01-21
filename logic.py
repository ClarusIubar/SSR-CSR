# 로직이 일어날 때, 알려줘야 된대. 그럼 로직은 따로 둬야겠지.
# 보고 하세요. 일꾼이여.

import json, urllib.parse
from error import HTTPStatus, ProtocolInterrupt

# 일할거면, A4용지는 있어야겠지.
storage = [] # 배열을 싫어하지만, sequence적인 자료에는 주효하니까 초기화 하자.
# monitor = None # 어떻게든 하면, 밖에 알려주겠지. # 관측소는 관측소에!

# do? act? CRUD? perform!
def perform_create(handler, req, res):
    length = int(handler.headers.get('Content-Length', 0)) # 있으면 n, 없으면 0
    raw = handler.rfile.read(length).decode('utf-8') if length > 0 else "" 
    # 없으면 빈칸, 있으면 읽어.
    
    # 바디
    req.body = json.loads(raw) if 'json' in (req.content_type or "") \
        else dict(urllib.parse.parse_qsl(raw))
    
    # 추출
    task = req.body.get('task')
    if not task: raise ProtocolInterrupt(HTTPStatus.BAD_REQUEST)
    
    # 저장
    storage.append(task)               # enum
    res.status_code, res.body = HTTPStatus.CREATED, {"msg": "saved"}

def perform_read(handler, req, res):   # enum
    res.status_code, res.body = HTTPStatus.OK, {"tasks": storage}

def perform_update(*args):
    return NotImplemented

def perform_delete(*args):
    return NotImplemented