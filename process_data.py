from typing import List
import pandas as pd
from json_types import TradeInfo


def pandify_prices(trades: List[TradeInfo]):
    x: List[int] = []
    y: List[float] = []
    for trade in trades:
        y.append(float(trade.p))
        x.append(trade.e)
    df = pd.DataFrame({"time (EST)": x, "price": y})
    return df


