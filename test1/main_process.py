import requests
from prettytable import PrettyTable
from datetime import datetime
from multiprocessing import Pool
from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['test1_lizanlycan_database']
tickers = db['pair_tickers']


def plot():
    ticks_api = tickers.find({"type": "api"})
    ticks_package = tickers.find({"type": "package"})

    buy_api_timestamp = []
    buy_api_price = []
    sell_api_timestamp = []
    sell_api_price = []

    buy_package_timestamp = []
    buy_package_price = []
    sell_package_timestamp = []
    sell_package_price = []

    for tick in ticks_api:
        buy_api_timestamp.append(tick["timestamp"])
        buy_api_price.append(tick["buy"])
        sell_api_timestamp.append(tick["timestamp"])
        sell_api_price.append(tick["sell"])

    for tick in ticks_package:
        buy_package_timestamp.append(tick["timestamp"])
        buy_package_price.append(tick["buy"])
        sell_package_timestamp.append(tick["timestamp"])
        sell_package_price.append(tick["sell"])

    plt.plot(buy_api_timestamp, buy_api_price, label='api-buy')
    plt.plot(buy_package_timestamp, buy_package_price, label='package-buy')
    plt.plot(sell_api_timestamp, sell_api_price, label='api-sell')
    plt.plot(sell_package_timestamp, sell_package_price, label='package-sell')

    plt.xlabel('Timestamp')
    plt.ylabel('Price')

    plt.title("Pair Tickers")

    plt.legend()

    plt.show()


def request_api(api, params, times):
    table = PrettyTable()
    for t in range(times):
        raw_data = requests.get(api).json()
        eth_btc = raw_data["eth_btc"] if "eth_btc" in raw_data else raw_data
        param_value = []

        # Pretty Table
        for param in params:
            if not isinstance(eth_btc[param], list):
                param_value.append(eth_btc[param])
            else:
                param_value.append(eth_btc[param][0][0])

        param_value.append(datetime.now().strftime("%M:%S:%f"))
        table.add_row(param_value)

        # Mongo DB
        ticker = {i: eth_btc[i] for i in params}
        ticker["pair"] = "eth_btc"
        ticker["timestamp"] = datetime.utcnow()
        ticker["type"] = "api" if "eth_btc" in raw_data else "package"
        tickers.insert_one(ticker)

    params.extend(["TIME"])
    table.field_names = map(lambda p: p.upper(), params)
    print(api)
    print(table)

# api = "https://api.tidex.com/api/3/ticker/eth_btc"


parallel_params = [("https://gate.tidex.com/api/tickers/3",
                    ["high", "low", "sell", "buy", "updated"], 10),
                   ("https://api.tidex.com/api/3/ticker/eth_btc",
                    ["high", "low", "sell", "buy", "updated"], 10)
                   ]

if __name__ == '__main__':
    pool = Pool(processes=2)
    pool.starmap(request_api, parallel_params)
    pool.close()
    pool.join()
    plot()
