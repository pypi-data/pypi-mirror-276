from typing import List

import requests
import time
import hmac
import hashlib
import json
import base64
import urllib.parse

API_URL = 'https://api.kraken.com'


def get_kraken_public_request(endpoint):
    response = requests.get(f'{API_URL}/0{endpoint}')
    if response.status_code != 200:
        raise ValueError(f"API request to {endpoint} returned {response.status_code}")
    return response.json()


class Kraken:
    def __init__(self, api_key: str, secret_key: str):
        self._api_key = api_key
        self._secret_key = secret_key

    def get_kraken_signature(self, urlpath: str, data, secret):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def post_kraken_private_request(self, uri_path, data):
        headers = {'API-Key': self._api_key, 'API-Sign': self.get_kraken_signature(uri_path, data, self._secret_key)}
        req = requests.post((API_URL + uri_path), headers=headers, data=data)
        if req.status_code != 200:
            raise ValueError(f"API error request to {uri_path} returned {req.status_code}")
        if req.json()["error"]:
            raise ValueError(f"{req.json()['error']}")
        print(req.json())
        return req

    def get_symbols(self) -> List[str]:
        data = get_kraken_public_request("/public/Assets")
        return data["result"]

    def get_asset_pairs(self) -> List[str]:
        """
        List of objects.

        Returns:

        Here's an example of object:
        ```
        "XETHXXBT": {
            "altname": ("ETHXBT", str),
            "wsname": ("ETH/XBT", str),
            "aclass_base": ("currency", str),
            "base": ("XETH", str),
            "aclass_quote": ("currency", str),
            "quote": ("XXBT", str),
            "lot": ("unit", str),
            "cost_decimals": (6, int),
            "pair_decimals": (5, int),
            "lot_decimals": (8, int),
            "lot_multiplier": (1, int),
            "leverage_buy": ([], List[int]),
            "leverage_sell": ([], List[int]),
            "fees": ([], List[List[float]]),
            "fees_maker": ([], List[List[float]]),
            "fee_volume_currency": ("ZUSD", str),
            "margin_call": (80, int),
            "margin_stop": (40, int),
            "ordermin": ("0.01", str),
            "costmin": ("0.00002", str),
            "tick_size": ("0.00001", str),
            "status": ("online", str),
            "long_position_limit": (550, int),
            "short_position_limit": (470, int)
        }
        ```
        """
        data = get_kraken_public_request("/public/AssetPairs")
        return data["result"]

    def get_spot_price(self, symbol: str):
        """
        Return best availabe ask price.

        a: Ask array, contains the following values:
            [0]: Price of the best available ask (lowest sell order price) as a string.
            [1]: Whole lot volume of the best available ask as a string.
            [2]: Lot volume of the best available ask as a string.

        b: Bid array, contains the following values:
            [0]: Price of the best available bid (highest buy order price) as a string.
            [1]: Whole lot volume of the best available bid as a string.
            [2]: Lot volume of the best available bid as a string.

        c: Last trade closed array, contains the following values:
            [0]: Price of the last trade as a string.
            [1]: Volume of the last trade as a string.

        v: Volume array, contains the following values:
            [0]: Today's traded volume as a string.
            [1]: Last 24 hours traded volume as a string.

        p: Volume weighted average price (VWAP) array, contains the following values:
            [0]: Today's VWAP as a string.
            [1]: Last 24 hours VWAP as a string.

        t: Number of trades array, contains the following values:
            [0]: Number of trades today as an integer.
            [1]: Number of trades in the last 24 hours as an integer.

        l: Low array, contains the following values:
            [0]: Today's lowest price as a string.
            [1]: Lowest price in the last 24 hours as a string.

        h: High array, contains the following values:
            [0]: Today's highest price as a string.
            [1]: Highest price in the last 24 hours as a string.

        o: The price at the start of the time period as a string.

        https://docs.kraken.com/rest/#tag/Market-Data/operation/getTickerInformation

        Args:
            symbol:

        Returns:

        """
        data = get_kraken_public_request(f"/public/Ticker?pair={symbol}")
        return float(data['result'][symbol]['a'][0])

    def buy_market_order(self, symbol, amount):
        nonce = int(time.time() * 1000)
        data = {
            'nonce': nonce,
            'pair': symbol,
            'type': 'buy',
            'ordertype': 'market',
            'volume': amount,
        }

        self.post_kraken_private_request("/0/private/AddOrder", data)
