
def testStock():
    from stockanalysis import Stock
    americanLithium = Stock(3.78, 3.96, 2)
    xiaomi = Stock(2.21, 3.40, 2)
    print(xiaomi)
    print(americanLithium)

import requests

s = requests.Session()
r = s.get("https://app.traderepublic.com/login")
data = {"phoneNumber": "+4917621482551","pin": "3053"}
s.options("https://api.traderepublic.com/api/v1/auth/web/login")
r = s.post("https://app.traderepublic.com/login", data)