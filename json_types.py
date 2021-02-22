
class TradeInfo:
    p: float
    e: int
    s: str

    def __init__(self, obj):
        self.e = obj["data"]["E"]
        self.s = obj["data"]["s"].lower()
        self.p = obj["data"]["p"]

