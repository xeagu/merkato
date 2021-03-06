import hashlib
import hmac
import json
import math
import requests
import time
import urllib.parse

from merkato.exchanges.exchange_base import ExchangeBase

DEBUG = True


class TuxExchange(ExchangeBase):
    url = "https://tuxexchange.com/api"

    def __init__(self, auth):
        self.privatekey = auth['privatekey']
        self.publickey  = auth['publickey']

    def sell(self, amount, ask, ticker):
        ''' Places a sell for a number of an asset at the indicated price (0.00000503 for example)
            :param amount: string
            :param ask: float
            :param ticker: string
        '''
        query_parameters = {
            "method": "sell",
            "market": "BTC",
            "coin": ticker,
            "amount": "{:.8f}".format(amount),
            "price": "{:.8f}".format(ask)
        }
        response = self._create_signed_request(query_parameters)

        return response['success']


    def buy(self, amount, bid, ticker):
        ''' Places a buy for a number of an asset at the indicated price (0.00000503 for example)
            :param amount: string
            :param bid: float
            :param ticker: string
        '''
        query_parameters = {
            "method": "buy",
            "market": "BTC",
            "coin": ticker,
            "amount": "{:.8f}".format(amount),
            "price": "{:.8f}".format(bid)
        }
        response = self._create_signed_request(query_parameters)

        return response['success']


    def get_all_orders(self, coin):
        ''' Returns all open orders for the ticker XYZ (not BTC_XYZ)
            :param coin: string
        '''
        # TODO: Accept BTC_XYZ by stripping BTC_ if it exists

        params = { "method": "getorders", "coin": coin }
        response = requests.get(self.url, params=params)

        response_json = json.loads(response.text)
        if DEBUG: print(response_json)
        return response_json


    def get_my_open_orders(self):
        ''' Returns all open orders for the authenticated user '''

        query_parameters = {
            "method": "getmyopenorders"
        }

        return self._create_signed_request(query_parameters)


    def cancel_order(self, order_id):
        ''' Cancels the order with the specified order ID
            :param order_id: string
        '''

        if DEBUG: print("--> Cancelling order...")

        if order_id == 0:
            if DEBUG: print("---> Order ID was zero, so bailing on function...")
            return False

        query_parameters = {
            "method": "cancelorder",
            "market": "BTC",
            "id": order_id
        }
        return self._create_signed_request(query_parameters)


    def get_ticker(self, coin="none"):
        ''' Returns the current ticker data for the given coin. If no coin is given,
            it will return the ticker data for all coins.
            :param coin: string (of the format BTC_XYZ)
        '''

        params = { "method": "getticker" }
        response = requests.get(self.url, params=params)

        if coin == "none":
            return json.loads(response.text)

        response_json = json.loads(response.text)
        print(response_json[coin])
        return response_json[coin]


    def get_24h_volume(coin="none"):
        ''' Returns the 24 hour volume for the given coin.
            If no coin is given, returns for all coins.
            :param coin string (of the form BTC_XYZ where XYZ is the alt ticker)
        '''

        params = { "method": "get24hvolume" }
        response = requests.get(self.url, params=params)

        if coin == "none":
            return json.loads(response.text)

        response_json = json.loads(response.text)
        print(response_json[coin])
        return response_json[coin]


    def get_balances(self, privatekey, publickey, coin='none'):
        # TODO: not exposed to base exchange class
        # also keys go unused, also coin...
        tuxParams = {"method" : "getmybalances"}

        response = self._create_signed_request(tuxParams)
        print(response)
        for crypto in response:
                print(str(crypto) + ": " + str(response[crypto]))

        return response


    def get_my_trade_history(self, start=0, end=0):
        if DEBUG: print("--> Getting trade history...")

        if start != 0 and end != 0:
            query_parameters = {
                "method": "getmytradehistory",
                "start": start,
                "end": end,
            }
        else:
            query_parameters = {
                "method": "getmytradehistory"
            }

        return self._create_signed_request(query_parameters)


    def _create_signed_request(self, query_parameters, nonce=None, timeout=15):
        ''' Signs provided query parameters with API keys
            :param query_parameters: dictionary
            :param nonce: int
            :param timeout: int
        '''

        # return response needing signature, nonce created if not supplied
        if not nonce:
            nonce = int(time.time() * 1000)

        query_parameters.update({"nonce": nonce})
        post = urllib.parse.urlencode(query_parameters)

        signature = hmac.new(self.privatekey.encode('utf-8'), post.encode('utf-8'), hashlib.sha512).hexdigest()
        head = {'Key': self.publickey, 'Sign': signature}

        response = requests.post(self.url, data=query_parameters, headers=head, timeout=timeout).json()
        return response
