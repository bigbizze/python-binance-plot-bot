from datetime import datetime
from typing import Tuple, Union, List
import pandas as pd
import aiomysql
import json

from aiomysql.utils import _PoolContextManager
from pymysql import escape_string

from json_types import TradeInfo

with open("./db.config", "r", encoding="utf-8") as fp:
    config = json.load(fp)


def select(symbol: str, time_str: str):
    if time_str.endswith("m"):
        interval, amount = "MINUTE", int(time_str.rstrip("m"))
    elif time_str.endswith("s"):
        interval, amount = "SECOND", int(time_str.rstrip("s"))
    else:
        return None, None
    ls = """select event_time, price from trades.{symbol} where event_time > DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL %s {time});""".format(
        symbol=escape_string(symbol).upper(),
        time=interval
    )

    return [
        amount,
        ls
    ]


class Poolio:
    def __init__(self, loop):
        self.loop = loop
        self.pool: _PoolContextManager

    @staticmethod
    def pre_process(symbol, data: Tuple[Tuple[Union[datetime, float]]]):
        out_data: List[TradeInfo] = []
        for line in data:
            out_data.append(TradeInfo.new(symbol=symbol, event_time=line[0], price=line[1]))
        return out_data

    @staticmethod
    def pandify_prices(trades: List[TradeInfo]):
        x: List[int] = []
        y: List[float] = []
        for trade in trades:
            y.append(float(trade.p))
            x.append(trade.e)
        df = pd.DataFrame({"time (EST)": x, "price": y})
        return df

    @staticmethod
    async def query_stuff(pool, symbol, time_str):
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                amount, select_statement = select(symbol, time_str)
                if amount is None:
                    return "Bad time given!"
                await cur.execute(select_statement, (amount,))
                print(cur.description)
                return await cur.fetchall()

    async def __aenter__(self):
        self.pool = await aiomysql.create_pool(host=config["host"], port=3306,
                                               user=config["username"], password=config["password"],
                                               db=config["database"], loop=self.loop)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        await self.pool.wait_closed()


async def query_stuff(loop, symbol, time_str, message):
    async with Poolio(loop) as poolio:
        result = await poolio.query_stuff(poolio.pool, symbol, time_str)
        if isinstance(result, str):
            return await message.channel.send("Bad time given!")
        return result



