from datetime import datetime


class TradeInfo:
    p: float
    e: int
    s: str
    dt: datetime

    def __init__(self, obj):
        self.dt = datetime.fromtimestamp(obj["data"]["E"] / 1000)
        self.e = obj["data"]["E"]
        self.s = obj["data"]["s"].lower()
        self.p = obj["data"]["p"]

