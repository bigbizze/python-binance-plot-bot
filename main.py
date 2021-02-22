# from queue import Queue
import multiprocessing as mp

from binance.websockets import Client

from cache_data import timed_data_cache
from discord_bot import discord_bot
from other import get_symbols
# from server import historical_data_server


MAX_MINUTES = 60


def main():
    client = Client()
    queue_pipe_store_to_request = mp.Queue()
    queue_request_from_store = mp.Queue()
    [symbol_with_ticker, symbols] = get_symbols(client)
    # p = mp.Process(target=historical_data_server, args=(symbols, queue_request_from_store, queue_pipe_store_to_request,))
    # p.start()
    p = mp.Process(target=discord_bot, args=(symbols, queue_request_from_store, queue_pipe_store_to_request,))
    p.start()
    timed_data_cache(client, symbol_with_ticker, symbols, queue_request_from_store, queue_pipe_store_to_request)


if __name__ == '__main__':
    main()




