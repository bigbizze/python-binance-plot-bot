from datetime import datetime
from copy import deepcopy


class Data:
    event_time: datetime
    e: str
    E: int
    s: str
    t: int
    p: str
    q: str
    b: int
    a: int
    T: int
    m: bool
    M: bool

    def __init__(self, obj):
        self.__dict__.update(obj)


class TradeInfo:
    stream: str
    data: Data

    def __init__(self, obj):
        self.data = Data(obj["data"])
        self.stream = obj["stream"]
        self.data.event_time = datetime.fromtimestamp(self.data.E / 1000)
        self.data.s = self.data.s.lower()

    def objectify(self):
        this = deepcopy(self)
        out_d = this.data.__dict__
        out_d["event_time"] = out_d["event_time"].strftime("%m/%d/%Y %H:%M:%S:%f")
        return out_d

