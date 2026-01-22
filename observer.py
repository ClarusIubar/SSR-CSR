# 뭔 시퀀스 핸들링이랑 오케스트레이션이여 지금은 사치야.
# 그냥 뭔 일이 일어나는지나 파악합시다.

import json
from enum import Enum, auto

# 이벤트를 정의해야 된다네.
class Event(Enum):
    INGEST = auto()  # 요청 수락
    PROCESS = auto() # 로직 집행
    EMIT = auto()    # 결과 방출
    SIGNAL = auto()  # 예외 포착

class Observer:
    # 옵저버 부모임.
    def update(self, event: Event, data: dict): # 데이터 형식만 지정해준 것 같네.
        pass # 오버라이딩 하나보네. 그럼 추상메서드로 강제해도 되는 거 아닌가?

class CLIObserver(Observer):
    # 터미널에 보여주는 용도임.
    def update(self, event, data):
        print(f" [DEBUG]CLI {event.name} >> {data}")

class BrowserObserver(Observer):
    # 브라우저 콘솔에 보여주는 용도임.
    def __init__(self): self.logs = [] # 얘는 로그로 전달하나 보다. CLI랑 다르네.
    def update(self, event, data):
        self.logs.append({"event": event.name, "data": data})
    def flush(self): # 모았다가 한번에 던지나? 로그를 던지는 게 별도로 있네.
        return json.dumps(self.logs, ensure_ascii=False)

class Subject:
    # 아 몰라, 서브젝트가 주체래. 옵저버 패턴에 필요한가벼.
    # 나는 날라리여. 정해주면 AI가 채워주겠지.
    # 코드짜는 거 구경할려.
    def __init__(self): self._observers = [] # 내부용도인가봐 _convention있네.
    def attach(self, obs): self._observers.append(obs) # 관측한 걸 append하나봐.
    def notify(self, event, data):
        for obs in self._observers:
            obs.update(event, data) # 옵저버에 저장된 걸 풀어서 업데이트 하나봐.

monitor = Subject() # 전역으로 선언하네 # 어디서든 append할 수 있게 하려나봐.

# 어, 새로운 클래스가 필요한가봐!
# 내가 모니터를 로직과 핸들러에 덕지덕지 붙이지 말라고 했더니 필요한가봐.
class Reconnaissance: # 이건 무슨뜻이지? / '정찰'이래. / 오오.
    def __init__(self, handler):
        self.handler = handler
        self.browser_obs = BrowserObserver()
        monitor.attach(CLIObserver())    # CLI는 바로 표현하고,
        monitor.attach(self.browser_obs) # 브라우저애 보내줄거는 다르게 표현하네!

    # 와 새로운 매직함수다!
    def __enter__(self):
        monitor.notify(Event.INGEST, {"path": self.handler.path})
        return self
    
    # 뭔가 끝나면 동작하는 건가봐.
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            monitor.notify(Event.SIGNAL, {"type": exc_type.__name__})
        # 시각적 구분선
        print("-" * 50)
        monitor._observers.clear() # 정찰종료!