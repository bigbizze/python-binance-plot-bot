import multiprocessing as mp

from binance.websockets import Client

from cache_data import timed_data_cache
from discord_bot import discord_bot
from other import get_symbols


def main():
    try:
        queue_pipe_store_to_request = mp.Queue()
        queue_request_from_store = mp.Queue()
        [symbol_with_ticker, symbols] = get_symbols()
        p = mp.Process(target=discord_bot, args=(symbols, queue_request_from_store, queue_pipe_store_to_request,))
        p.start()
        timed_data_cache(symbols, symbol_with_ticker, queue_request_from_store, queue_pipe_store_to_request)
    except Exception as e:
        with open("main_error.log", "a") as fp:
            fp.write(repr(e))


if __name__ == '__main__':
    main()




