import asyncio
import io
from datetime import datetime, timedelta
from multiprocessing.queues import Queue
import discord

from asyncio_mysql import query_stuff
from plotting import get_line_plot
from process_data import pre_process

MAX_MINUTES = 60 * 12


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
        # queue_request_from_store: Queue,
        # queue_pipe_store_to_request: Queue,
):
    with open("config", "r", encoding="utf-8") as fp:
        token = fp.read()

    client = discord.Client()

    async def task():
        await client.wait_until_ready()
        while True:
            await asyncio.sleep(1)
            # print('Running')

    def handle_exit():
        print("Handling")
        client.loop.run_until_complete(client.logout())
        for t in asyncio.Task.all_tasks(loop=client.loop):
            if t.done():
                t.exception()
                continue
            t.cancel()
            try:
                client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
                t.exception()
            except asyncio.InvalidStateError:
                pass
            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                pass

    while True:
        try:

            @client.event
            async def on_message(message):
                if message.author == client.user:
                    return
                if not message.content.startswith('.plot'):
                    return
                if not message.channel.id == 809144516513628250:
                    return
                args = message.content.split(" ")
                if len(args) < 2:
                    return await message.channel.send("No symbol? lmao")
                symbol = args[1]
                symbol = symbol.lower()
                symbol = symbol if symbol.endswith("btc") else f"{symbol}btc"
                if symbol not in symbols:
                    return await message.channel.send(f"You gave us {symbol} which is not a valid symbol!")
                last = args[2] if len(args) == 3 else None
                if last is None:
                    return await message.channel.send("Bad time argument!")
                data = await query_stuff(
                    loop=client.loop,
                    message=message,
                    symbol=symbol,
                    time_str=last
                )
                df = pre_process(symbol, data)
                buffer: io.BytesIO = get_line_plot(symbol, df)
                if data is None:
                    return await message.channel.send("No trades found{0}!".format(f" in the last {args[2]}" if last is not None else ""))
                file = discord.File(buffer, "plot.png")
                await message.channel.send(file=file)

            client.loop.create_task(task())
            try:
                client.loop.run_until_complete(client.start(token))
            except Exception as e:
                from contextlib import redirect_stdout
                with open('discord_error.log', 'w') as f:
                    with redirect_stdout(f):
                        print(repr(e))
                # with open("discord_error.log", "a") as fp:
                #     fp.write(repr(e))
                handle_exit()
            # client.run(token)
        except Exception as e:
            with open("discord_error.log", "a") as fp:
                fp.write(repr(e))
