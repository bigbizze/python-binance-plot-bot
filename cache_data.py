import time
from datetime import datetime, timedelta
from typing import Dict, List

from binance.websockets import BinanceSocketManager, Client

from process_data import pandify_prices
from json_types import TradeInfo
import multiprocessing as mp
from threading import Thread
from queue import Queue, Empty

from plotting import get_line_plot


def get_symbol_store(symbols) -> Dict[str, List[TradeInfo]]:
    symbol_store: Dict[str, List[TradeInfo]] = dict()
    for symbol in symbols:
        symbol_store[symbol] = []
    return symbol_store


def clean_filter(x: TradeInfo):
    return datetime.now() < x.dt + timedelta(minutes=30)


def get_over_interval_filter(interval: datetime):
    def over_interval_filter(x: TradeInfo):
        return x.dt > interval
    return over_interval_filter


def clean_store(symbol_store: Dict[str, List[TradeInfo]]) -> Dict[str, List[TradeInfo]]:
    store_items = symbol_store.items()
    start_len = sum([len(v) for k, v in store_items])
    for k, v in store_items:
        symbol_store[k] = list(filter(clean_filter, symbol_store[k]))
    print("s: {0}, e: {1}".format(start_len, sum([len(v) for k, v in symbol_store.items()])))
    return symbol_store


def store_manager(symbols: List[str], q_to_store: Queue, q_request_from_store: mp.Queue, q_pipe_store_to_request: mp.Queue):
    try:
        symbol_store = get_symbol_store(symbols)
        last_garbage_clean = time.time()
        while True:
            try:
                trade: TradeInfo = q_to_store.get(block=True, timeout=0.1)
                symbol_store[trade.s].append(trade)
                # symbol_store = clean_store_for_symbol(trade, symbol_store)
            except Empty:
                pass
            try:
                [symbol, interval] = q_request_from_store.get(block=True, timeout=0.1)
                if symbol is not None:
                    symbol_list = symbol_store[symbol]
                    symbol_list = symbol_list if interval is None else list(filter(get_over_interval_filter(interval), symbol_list))
                    data_frame = pandify_prices(symbol_list)
                    if not data_frame.empty and data_frame.shape[0] > 1:
                        base_64 = get_line_plot(symbol, data_frame)
                        q_pipe_store_to_request.put(base_64)
                    else:
                        q_pipe_store_to_request.put(None)
            except Empty:
                pass
            if time.time() - last_garbage_clean > 300:
                symbol_store = clean_store(symbol_store)
                last_garbage_clean = time.time()
    except Exception as e:
        with open("store_manager_error.log", "a") as fp:
            fp.write(repr(e))


def get_msg_processor(q_to_store: Queue):
    # start = datetime.now()

    def process_m_message(msg):
        trade = TradeInfo(msg)
        # next_time = datetime.now()
        # print("t: {0}".format((next_time - start).seconds))
        q_to_store.put(trade)
    return process_m_message


def ws_socko(
        queue_to_store: mp.Queue,
        symbol_with_ticker: List[str],
):
    process_m_message = get_msg_processor(queue_to_store)
    client = Client()
    bm = BinanceSocketManager(client)
    # pass a list of stream names
    # noinspection PyTypeChecker
    bm.start_multiplex_socket(symbol_with_ticker, process_m_message)
    bm.start()


def timed_data_cache(
        symbols: List[str],
        symbol_with_ticker: List[str],
        queue_request_from_store: mp.Queue,
        queue_pipe_store_to_request: mp.Queue
):
    queue_to_store = Queue()
    num_threads = 5
    divisor = len(symbol_with_ticker) // num_threads
    threads: List[Thread] = []
    for i in range(num_threads):
        threads.append(Thread(target=ws_socko, args=(queue_to_store, symbol_with_ticker[i * divisor: (i + 1) * divisor])))
    [x.start() for x in threads]
    t = Thread(target=store_manager, args=(symbols, queue_to_store, queue_request_from_store, queue_pipe_store_to_request,))
    t.start()




