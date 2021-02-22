from datetime import datetime


class TradeInfo:
    p: float
    e: int
    s: str
    dt: datetime

    @staticmethod
    def new(symbol, event_time, price):
        return TradeInfo({
            "data": {
                "E": event_time,
                "s": symbol,
                "p": price
            }
        })

    def __init__(self, obj):
        self.dt = obj["data"]["E"]
        self.e = int(datetime.timestamp(obj["data"]["E"]))
        self.s = obj["data"]["s"].lower()
        self.p = obj["data"]["p"]

