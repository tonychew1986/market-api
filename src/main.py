import os
import time
import sys, getopt
import datetime
import math
import threading
import logging
import socket

import redis

import os
from os.path import join, dirname
from dotenv import load_dotenv

#dotenv_path = join('../.env')
# load_dotenv('.env')

if(os.path.exists("/etc/rockx/.env")):
    load_dotenv('/etc/rockx/.env')
    print("/etc/rockx/.env")
else:
    load_dotenv('.env')
    print(".env")

redis_host = os.environ.get("REDIS_HOST")
redis_port = os.environ.get("REDIS_PORT")
redis_password = os.environ.get("REDIS_PASSWORD")

from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

trackedCoins = [
    "ATOM", "BTC", "ETH", "USDT"
]
baseCoins = [
    "USD", "BTC", "CNY", "USDT"
]

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

class GetPrices(Resource):
    def get(self):
        parser.add_argument('pairs', type=str, action='append')
        parser.add_argument('base_currency', type=str)
        args = parser.parse_args()

        print("------------")
        pairs = args['pairs']
        result = pairs[0].split(',')

        priceCollection = []
        defaultBaseExchangeRate = 7
        defaultBaseExchangeRateUSD = 1
        defaultBaseExchangeRateBTC = 9000

        for i in result:
            print("------------")
            quotedCurrency = i.lower()

            print("------------")

            defaultBaseExchangeRateUSD = 1
            defaultBaseExchangeRateBTC = 1/float(r.get("btc:usd:average_price"))

            template = {}
            quotedCurrencyCollection = []

            btcBasePairData = {
              "name": "BTC",
              "average_buy_price": r.get(quotedCurrency + ":btc:average_buy"),
              "average_sell_price": r.get(quotedCurrency + ":btc:average_sell"),
              "average_market_price": r.get(quotedCurrency + ":btc:average_price"),
            }

            usdBasePairData = {
              "name": "USD",
              "average_buy_price": r.get(quotedCurrency + ":usd:average_buy"),
              "average_sell_price": r.get(quotedCurrency + ":usd:average_sell"),
              "average_market_price": r.get(quotedCurrency + ":usd:average_price"),
            }

            quotedCurrencyCollection.append(btcBasePairData)
            quotedCurrencyCollection.append(usdBasePairData)

            indicatedBaseCurrency = args['base_currency'].lower()
            indicatedBasePairData = {
              "name": args['base_currency'],
              "average_buy_price": r.get(quotedCurrency + ":" + indicatedBaseCurrency +":average_buy"),
              "average_sell_price": r.get(quotedCurrency + ":" + indicatedBaseCurrency +":average_sell"),
              "average_market_price": r.get(quotedCurrency + ":" + indicatedBaseCurrency +":average_price"),
            }

            if(indicatedBaseCurrency != "usd"):
                quotedCurrencyCollection.append(indicatedBasePairData)

            template = {
                "name": i,
                # "exchanges": price[4],
                "trading_price": quotedCurrencyCollection,
            }


            priceCollection.append(template)


        print("priceCollection", priceCollection)




        return {
            "success": "true",
            "data": {
                "default_currency": "USD | BTC",
                # "default_base_exchange_rate_usd": defaultBaseExchangeRateUSD,
                # "default_base_exchange_rate_btc": defaultBaseExchangeRateBTC,
                "price": priceCollection
            }
        }


api.add_resource(GetPrices, '/v1/markets/')



if __name__ == '__main__':
    app.run(debug=True)
