from typing import Self
from LNS_stock import Stock

Stock.update_local_data()
stocks = Stock.get_stocks_from_watchlist()
