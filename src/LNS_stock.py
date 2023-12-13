import csv
import json
import os
from typing import List

import requests
from bs4 import BeautifulSoup


class LnsStock:
    url: str
    api_id: str
    wkn: str
    isin: str
    name: str
    data: list
    filepath: str

    def __init__(
        self, url=None, api_id=None, wkn=None, isin=None, name=None, filepath=None
    ) -> None:
        self.url = url
        self.api_id = api_id
        self.wkn = wkn
        self.isin = isin
        self.name = name
        self.filepath = filepath
        self.data = None

    def get_stock_from_url(url: str):
        stock = LnsStock()
        stock.url = url
        resp = requests.get(url)
        html = resp.content.decode(encoding="UTF-8")
        soup = BeautifulSoup(html, "html.parser")
        stock.soup = soup
        stock.api_id = LnsStock.__get_api_id(soup)
        stock.name = LnsStock.__get_stock_name(soup)
        stock.isin = LnsStock.__get_stock_isin(soup)
        stock.wkn = LnsStock.__get_stock_wkn(soup)
        stock.filepath = "./stocks/" + stock.isin + ".csv"
        return stock

    def get_stocks_from_watchlist():
        stock_objs:list[LnsStock] = []
        with open("./stocks/watchlist.json", "r") as f:
            stocks_dict = json.loads(f.read())["stocks"]

        for stock_dict in stocks_dict:
            stock_obj = LnsStock(
                url=stock_dict["url"],
                api_id=stock_dict["api_id"],
                wkn=stock_dict["wkn"],
                isin=stock_dict["isin"],
                name=stock_dict["name"],
                filepath=stock_dict["filepath"],
            )
            if os.path.exists(stock_obj.filepath):
                with open(stock_obj.filepath, "r") as f:
                    reader = csv.reader(f, delimiter=",")
                    data = []
                    for l in reader:
                        data.append((l[0].strip(), l[1].strip()))
                    stock_obj.data = data
            stock_objs.append(stock_obj)
        return stock_objs

    def __get_api_id(soup: BeautifulSoup):
        res = soup.find_all("span")
        for span in res:
            # print(span)
            if (
                span.get("item") != None
                and span.get("item") != ""
                and span.get("source") == "lightstreamer"
                and span.get("table") == "quotes"
                and span.get("field") == "mid"
            ):
                lang_schwarz_api_id = span.get("item")[:-2]
                break
        return lang_schwarz_api_id

    def __get_stock_name(soup: BeautifulSoup):
        title = soup.find_all("h3")[0].text.strip()
        idx = 0 if "Watchlist" in title.split("\n\n")[1] else 1
        return title.split("\n\n")[idx].split('DL-')[0].split('DL -')[0].strip()

    def __get_stock_wkn(soup: BeautifulSoup):
        return (
            soup.select(
                "div.mpe_bootstrapgrid.col-sm-6.informerhead.informerhead-half.no-padding"
            )[0]
            .text.split("|")[1]
            .split("WKN:")[1]
            .split("\n")[0]
            .strip()
        )

    def __get_stock_isin(soup: BeautifulSoup):
        return (
            soup.select(
                "div.mpe_bootstrapgrid.col-sm-6.informerhead.informerhead-half.no-padding"
            )[0]
            .text.split("|")[0]
            .split("ISIN:")[1]
            .strip()
        )

    def save_in_watchlist(self):
        self.filepath = (
            self.filepath if self.filepath else "./stocks/" + self.isin + ".csv"
        )
        data = {
            "name": self.name,
            "url": self.url,
            "api_id": self.api_id,
            "isin": self.isin,
            "wkn": self.wkn,
            "filepath": self.filepath,
        }

        current_watchlist = {}
        if os.path.exists("./stocks/watchlist.json"):
            with open("./stocks/watchlist.json", "r") as file:
                current_watchlist = json.load(file)

        if "stocks" in current_watchlist.keys():
            if (
                len(
                    list(
                        filter(
                            lambda obj: obj["api_id"] == self.api_id,
                            current_watchlist["stocks"],
                        )
                    )
                )
                == 0
            ):
                current_watchlist["stocks"].append(data)
            else:
                for i, stock in enumerate(current_watchlist["stocks"]):
                    if stock["wkn"] == self.wkn:
                        current_watchlist["stocks"][i] = data
                        break
        else:
            current_watchlist["stocks"] = [data]
        with open("./stocks/watchlist.json", "w") as file:
            json.dump(current_watchlist, file, indent=4)

    def load_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"
        }
        data = {
            "container": "chart1",
            "instrumentId": self.api_id,
            "marketId": 1,
            "quotetype": "mid",
            "series": "intraday,history,flags",
            "type": "",
            "localeId": "1",
        }
        url = "https://www.ls-tc.de/_rpc/json/instrument/chart/dataForInstrument"

        resp = requests.get(url=url, params=data, headers=headers)

        series = []
        with open(self.filepath, "w") as f:
            for part in resp.json()["series"]["history"]["data"]:
                line = (part[0], part[1])
                series.append(line)
                f.writelines(str(line[0]) + ", " + str(line[1]) + "\n")
        self.data = series

    def __str__(self) -> str:
        keys = list(self.__dict__.keys())
        if "soup" in keys:
            keys.remove("soup")
        d = {}
        for key in keys:
            d[key] = self.__dict__[key]
        return str(d)

    def update_local_data() -> None:
        for stock in LnsStock.get_stocks_from_watchlist():
            stock.load_data()
