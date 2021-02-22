import json
from datetime import datetime
from typing import List, Tuple, Union
import pandas as pd
from json_types import TradeInfo


def pre_process(symbol, data: Tuple[Tuple[Union[datetime, float]]]):
    out_data: List[TradeInfo] = []
    log_data = ""
    for line in data:
        trade_info = TradeInfo.new(symbol=symbol, event_time=line[0], price=line[1])
        out_data.append(trade_info)
        log_data += f"\nprice:{trade_info.p}, time:{trade_info.e}\n"
    with open("/root/data.log", "a", encoding="utf-8") as fp:
        fp.write(f"\n\n{log_data}\n\n")
    return pandify_prices(out_data)


def pandify_prices(trades: List[TradeInfo]):
    x: List[int] = []
    y: List[float] = []
    for trade in trades:
        y.append(float(trade.p))
        x.append(trade.e)
    df = pd.DataFrame({"time (EST)": x, "price": y})
    return df


