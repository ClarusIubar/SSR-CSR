# 로직이 일어날 때, 알려줘야 된대. 그럼 로직은 따로 둬야겠지.
# 보고 하세요. 일꾼이여.

import json, urllib.parse
from error import HTTPStatus, ProtocolInterrupt

# 일할거면, A4용지는 있어야겠지.
storage = [] # 배열을 싫어하지만, sequence적인 자료에는 주효하니까 초기화 하자.
# monitor = None # 어떻게든 하면, 밖에 알려주겠지. # 관측소는 관측소에!

# do? act? CRUD? perform!
def perform_create(req, res):
    # 바디 읽기/파싱은 이미 핸들러가 _fill_request에서 다 해놨어.
    # 우리는 차려진 밥상(req.body)에서 먹기만 하면 돼.
    
    # 추출
    task = req.body.get('task')        # enum
    if not task: raise ProtocolInterrupt(HTTPStatus.BAD_REQUEST, "어라!")
    
    # 저장
    storage.append(task)               # enum
    res.status_code, res.body = HTTPStatus.CREATED, {"msg": "저장됨."}

def perform_read(req, res):   
    # 여기도 핸들러는 필요 없지.         # enum
    res.status_code, res.body = HTTPStatus.OK, {"tasks": storage}

def perform_update(req, res):
    # 수정할 놈이 몇 번째인지(index), 뭘로 바꿀 건지(task) 가져와.
    try:
        idx = int(req.body.get('index'))
        new_task = req.body.get('task')
        
        # 없는 번호를 건드리면 혼내줘야지.
        if not (0 <= idx < len(storage)):
            raise ProtocolInterrupt(HTTPStatus.NOT_FOUND, "잘못된 범위요!")
        
        storage[idx] = new_task
        res.status_code, res.body = HTTPStatus.OK, {"msg": "수정됨.", "index": idx}
        
    except (ValueError, TypeError):
        raise ProtocolInterrupt(HTTPStatus.BAD_REQUEST, "뭔가 잘못했는디.")

def perform_delete(req, res):
    # 지울 놈 번호(index) 가져와.
    try:
        idx = int(req.body.get('index'))
        
        if not (0 <= idx < len(storage)):
            raise ProtocolInterrupt(HTTPStatus.NOT_FOUND, "잘못된 범위요!")
        
        removed_item = storage.pop(idx)
        res.status_code, res.body = HTTPStatus.OK, {"msg": "삭제됨.", "item": removed_item}
        
    except (ValueError, TypeError):
        raise ProtocolInterrupt(HTTPStatus.BAD_REQUEST, "뭔가 잘못했는디.")