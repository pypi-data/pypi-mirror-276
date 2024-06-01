# -*- coding:utf-8 -*-

"""
Market module.

Project: alphahunter
Author: HJQuant
Description: Asynchronous driven quantitative trading framework
"""

import json

from quant import const
from quant.utils import logger


class Ticker:
    """ Ticker object.

    Args:
        platform: Exchange platform name, e.g. binance/bitmex.
        symbol: Trade pair name, e.g. ETH/BTC.
        ask: 市场当前最优卖价
        bid: 市场当前最优买价
        last:市场最新成交价
        timestamp: Update time, millisecond.
    """
    
    def __init__(self, platform=None, symbol=None, ask=None, bid=None, last=None, timestamp=None):
        """ Initialize. """
        self.platform = platform
        self.symbol = symbol
        self.ask = ask
        self.bid = bid
        self.last = last
        self.timestamp = timestamp

    @property
    def data(self):
        d = {
            "platform": self.platform,
            "symbol": self.symbol,
            "ask": self.ask,
            "bid": self.bid,
            "last": self.last,
            "timestamp": self.timestamp
        }
        return d

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)    


class Orderbook:
    """ Orderbook object.

    Args:
        platform: Exchange platform name, e.g. binance/bitmex.
        symbol: Trade pair name, e.g. ETH/BTC.
        asks: Asks list, e.g. [[price, quantity], [...], ...]
        bids: Bids list, e.g. [[price, quantity], [...], ...]
        timestamp: Update time, millisecond.
    """

    def __init__(self, platform=None, symbol=None, asks=None, bids=None, timestamp=None):
        """ Initialize. """
        self.platform = platform
        self.symbol = symbol
        self.asks = asks
        self.bids = bids
        self.timestamp = timestamp

    @property
    def data(self):
        d = {
            "platform": self.platform,
            "symbol": self.symbol,
            "asks": self.asks,
            "bids": self.bids,
            "timestamp": self.timestamp
        }
        return d

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)


class Trade:
    """ Trade object.

    Args:
        platform: Exchange platform name, e.g. binance/bitmex.
        symbol: Trade pair name, e.g. ETH/BTC.
        action: Trade action, BUY or SELL.
        price: Order place price.
        quantity: Order place quantity.
        timestamp: Update time, millisecond.
    """

    def __init__(self, platform=None, symbol=None, action=None, price=None, quantity=None, timestamp=None):
        """ Initialize. """
        self.platform = platform
        self.symbol = symbol
        self.action = action
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp

    @property
    def data(self):
        d = {
            "platform": self.platform,
            "symbol": self.symbol,
            "action": self.action,
            "price": self.price,
            "quantity": self.quantity,
            "timestamp": self.timestamp
        }
        return d

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)


class Kline:
    """ Kline object.

    Args:
        platform: Exchange platform name, e.g. binance/bitmex.
        symbol: Trade pair name, e.g. ETH/BTC.
        open: Open price.
        high: Highest price.
        low: Lowest price.
        close: Close price.
        volume: Total trade volume.
        timestamp: Update time, millisecond.
        kline_type: Kline type name, kline - 1min, kline_5min - 5min, kline_15min - 15min.
    """

    def __init__(self, platform=None, symbol=None, open=None, high=None, low=None, close=None, volume=None,
                 timestamp=None, kline_type=None, **kwargs):
        """ Initialize. """
        self.platform = platform
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.timestamp = timestamp
        self.kline_type = kline_type
        for (k, v) in kwargs.items(): #如果是自合成K线的话就填充剩余字段
            setattr(self, k, v)

    @property
    def data(self):
        d = {
            "platform": self.platform,
            "symbol": self.symbol,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "timestamp": self.timestamp,
            "kline_type": self.kline_type
        }
        for (k, v) in vars(self).items(): #如果是自合成K线的话就填充剩余字段
            if not k.startswith('__') and k not in d:
                d[k] = v
        return d

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)

    def is_custom(self):
        """ 判断是自合成K线还是交易所提供的K线
        """
        return hasattr(self, "usable")

    def is_custom_and_usable(self):
        """ 判断是自合成K线同时可用
        """
        return hasattr(self, "usable") and self.usable


class Market:
    """ Subscribe Market.

    Args:
        market_type: Market data type,
            MARKET_TYPE_TRADE = "trade"
            MARKET_TYPE_ORDERBOOK = "orderbook"
            MARKET_TYPE_KLINE = "kline"
            MARKET_TYPE_KLINE_5M = "kline_5m"
            MARKET_TYPE_KLINE_15M = "kline_15m"
            MARKET_TYPE_TICKER = "ticker"
        platform: Exchange platform name, e.g. binance/bitmex.
        symbol: Trade pair name, e.g. ETH/BTC.
        callback: Asynchronous callback function for market data update.
                e.g. async def on_event_kline_update(kline: Kline):
                        pass
    """

    def __init__(self, market_type, platform, symbol, callback):
        """ Initialize. """
        if platform == "#" or symbol == "#":
            multi = True
        else:
            multi = False
        if market_type == const.MARKET_TYPE_ORDERBOOK:
            from quant.event import EventOrderbook
            EventOrderbook(platform, symbol).subscribe(callback, multi)
        elif market_type == const.MARKET_TYPE_TRADE:
            from quant.event import EventTrade
            EventTrade(platform, symbol).subscribe(callback, multi)
        elif market_type in [const.MARKET_TYPE_KLINE, const.MARKET_TYPE_KLINE_5M, const.MARKET_TYPE_KLINE_15M]:
            from quant.event import EventKline
            EventKline(platform, symbol, kline_type=market_type).subscribe(callback, multi)
        elif market_type == const.MARKET_TYPE_TICKER:
            from quant.event import EventTicker
            EventTicker(platform, symbol).subscribe(callback, multi)
        else:
            logger.error("market_type error:", market_type, caller=self)
