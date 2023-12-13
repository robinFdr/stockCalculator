from typing import Self

from LNS_stock import LnsStock

LnsStock.update_local_data()
stocks = LnsStock.get_stocks_from_watchlist()
