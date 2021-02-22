from typing import Optional

from binance.websockets import Client


def get_symbols(client: Optional[Client] = None):
    _client = client if client is not None else Client()
    symbol_with_ticker = []
    symbols = []
    for symbol in _client.get_exchange_info()["symbols"]:
        if not symbol["symbol"].endswith("BTC"):
            continue
        symbol = symbol["symbol"].lower()
        symbols.append(symbol)
        symbol_with_ticker.append(f"{symbol}@trade")
    return [symbol_with_ticker, symbols]


