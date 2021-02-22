import io
from datetime import datetime, timedelta
from multiprocessing.queues import Queue
import discord

MAX_MINUTES = 60


def process_last(last: str):
    try:
        if last.endswith("m"):
            last = int(last.rstrip("m"))
            if last > MAX_MINUTES:
                return f"We only store data from the last {MAX_MINUTES} minutes!"
            return datetime.now() - timedelta(minutes=last)
        if last.endswith("s"):
            last = int(last.rstrip("s"))
            return datetime.now() - timedelta(seconds=last)
    except:
        pass
    return "Time argument must be in the format of `10m` or `45s`"


def discord_bot(
        symbols,
        queue_request_from_store: Queue,
        queue_pipe_store_to_request: Queue,
):
    client = discord.Client()

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if not message.content.startswith('.plot'):
            return
        args = message.content.split(" ")
        if len(args) < 2:
            return await message.channel.send("No symbol? lmao")
        symbol = args[1]
        symbol = symbol.lower()
        symbol = symbol if symbol.endswith("btc") else f"{symbol}btc"
        if symbol not in symbols:
            return await message.channel.send(f"You gave us {symbol} which is not a valid symbol!")
        last = process_last(args[2]) if len(args) == 3 else None
        if isinstance(last, str):
            return await message.channel.send(last)
        queue_request_from_store.put([symbol, last])
        data: io.BytesIO = queue_pipe_store_to_request.get()
        if data is None:
            return await message.channel.send("No trades found{0}!".format(f" in the last {args[2]}" if last is not None else ""))
        file = discord.File(data, "plot.png")
        await message.channel.send(file=file)

    with open("config", "r", encoding="utf-8") as fp:
        token = fp.read()
    client.run(token)