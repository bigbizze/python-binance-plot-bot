from datetime import datetime
from typing import List
import pandas as pd
from json_types import TradeInfo


def pandify_prices(trades: List[TradeInfo]):
    x: List[int] = []
    y: List[float] = []
    for trade in trades:
        y.append(float(trade.data.p))
        x.append(trade.data.E)
    df = pd.DataFrame({"time (EST)": x, "price": y})
    return df


# def pandify_prices2(trades: List[TradeInfo]):
#     x: List[int] = []
#     y: List[float] = []
#     prices: List[float] = []
#     num_trades = len(trades)
#     last_time = None
#     for i, trade in enumerate(trades):
#         next_time = int(datetime.timestamp(trade.data.event_time))
#         last_time = next_time if last_time is None else last_time
#         if (next_time != last_time and i != 0) or (i - 1 == num_trades):
#             avg_price = sum(prices) / len(prices)
#             y.append(avg_price)
#             x.append(last_time)
#             prices = []
#             last_time = next_time
#         prices.append(float(trade.data.p))
#     df = pd.DataFrame({"time (EST)": x, "price": y})
#     return df
