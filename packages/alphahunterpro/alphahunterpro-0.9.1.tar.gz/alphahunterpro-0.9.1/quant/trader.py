# -*- coding:utf-8 -*-

"""
Trader Module.

Project: alphahunter
Author: HJQuant
Description: Asynchronous driven quantitative trading framework
"""

import copy
from collections import defaultdict

from quant import const
from quant.state import State
from quant.utils import logger
from quant.tasks import SingleTask
from quant.order import Fill, Order, ORDER_TYPE_LIMIT
from quant.position import Position
from quant.event import EventOrder
from quant.gateway import ExchangeGateway
from quant.market import Kline, Orderbook, Trade, Ticker
from quant.asset import Asset


def gateway_class(platform):
    """获取对应的交易网关类
    
    Args:
        platform: 交易平台名称
    
    Returns:
        交易网关类
    """
    if platform == const.DATAMATRIX:
        from quant.datamatrix import DataMatrixTrader as T
        return T
    elif platform == const.BACKTEST:
        from quant.backtest import BacktestTrader as T
        return T
    elif platform == const.OKEX:
        from quant.platform.okex import OKExTrader as T
        return T
    #elif platform == const.OKEX_MARGIN:
    #    from quant.platform.okex_margin import OKExMarginTrader as T
    #    return T
    #elif platform == const.OKEX_FUTURE:
    #    from quant.platform.okex_future import OKExFutureTrader as T
    #    return T
    #elif platform == const.OKEX_SWAP:
    #    from quant.platform.okex_swap import OKExSwapTrader as T
    #    return T
    #elif platform == const.BITMEX:
    #    from quant.platform.bitmex import BitmexTrader as T
    #    return T
    #elif platform == const.BINANCE:
    #    from quant.platform.binance import BinanceTrader as T
    #    return T
    #elif platform == const.BINANCE_FUTURE:
    #    from quant.platform.binance_future import BinanceFutureTrader as T
    #    return T
    elif platform == const.HUOBI:
        from quant.platform.huobi import HuobiTrader as T
        return T
    elif platform == const.HUOBI_FUTURE:
        from quant.platform.huobi_future import HuobiFutureTrader as T
        return T
    #elif platform == const.GATE:
    #    from quant.platform.gate import GateTrader as T
    #    return T
    elif platform == const.FTX:
        from quant.platform.ftx import FTXTrader as T
        return T
    else:
        return None


class Trader(ExchangeGateway):
    """ Trader Module.
    """

    class MAPPING_LAYER:
        """ 符号映射转换相关
        """
        def __init__(self):
            self.map_dict = None #符号映射字典
            self.is_upper = None #币种是否大写


    def __init__(self, **kwargs):
        """initialize trader object.
        
        Args:
            strategy: 策略名称,由哪个策略发起
            platform: 交易平台
            databind: 这个字段只有在platform等于datamatrix或backtest的时候才有用,代表为矩阵操作或策略回测提供历史数据的交易所
            symbols: 策略需要订阅和交易的符号
            account: 交易所登陆账号,如果为空就只是订阅市场公共行情数据,不进行登录认证,所以也无法进行交易等
            access_key: 登录令牌
            secret_key: 令牌密钥
            cb: ExchangeGateway.ICallBack {
                on_state_update_callback: `状态变化`(底层交易所接口,框架等)通知回调函数
                on_kline_update_callback: `K线数据`通知回调函数 (值为None就不启用此通知回调)
                on_orderbook_update_callback: `订单簿深度数据`通知回调函数 (值为None就不启用此通知回调)
                on_trade_update_callback: `市场最新成交`通知回调函数 (值为None就不启用此通知回调)
                on_ticker_update_callback: `市场行情tick`通知回调函数 (值为None就不启用此通知回调)
                on_order_update_callback: `用户挂单`通知回调函数 (值为None就不启用此通知回调)
                on_fill_update_callback: `用户挂单成交`通知回调函数 (值为None就不启用此通知回调)
                on_position_update_callback: `用户持仓`通知回调函数 (值为None就不启用此通知回调)
                on_asset_update_callback: `用户资产`通知回调函数 (值为None就不启用此通知回调)
            }
        """
        T = gateway_class(kwargs["platform"]) #找到指定的交易接口类
        if T == None:
            logger.error("platform not found:", kwargs["platform"], caller=self)
            cb = kwargs["cb"]
            SingleTask.run(cb.on_state_update_callback, State(kwargs["platform"], kwargs.get("account"), "platform not found"))
            return
        #------------------------------------------------
        #符号映射转换相关
        self.is_upper = False #币种符号是否转换成大写
        self.system_to_native = {} #'量化平台通用交易符号'转换成'交易所原始符号'
        self.native_to_system = {} #'交易所原始符号'转换成'量化平台通用交易符号'
        layer = T.mapping_layer() #从交易所获取符号转换层信息
        if layer:
            self.system_to_native = layer.map_dict #'交易对'符号映射信息,类似 BTC/USDT -> btcusdt
            self.is_upper = layer.is_upper #'币种'符号是否大写,类似 btc -> BTC
            for (k, v) in self.system_to_native.items(): #生成逆转换映射信息,类似 btcusdt -> BTC/USDT
                self.native_to_system[v] = k
        #符号转换
        if self.system_to_native: #存在映射信息,意味着启用了符号转换功能
            native_symbol = []
            for sym in kwargs["symbols"]:
                if not self.system_to_native.get(sym): #如果符号映射信息中没有,返回错误
                    logger.error("symbols not found:", kwargs["symbols"], caller=self)
                    cb = kwargs["cb"]
                    SingleTask.run(cb.on_state_update_callback, State(kwargs["platform"], kwargs.get("account"), "symbols not found"))
                    return
                native_symbol.append(self.system_to_native[sym])
            kwargs["symbols"] = native_symbol
        #映射功能启用就需要hook回调函数
        if self.system_to_native or self.is_upper:
            self.hookCB(kwargs["cb"])
        #
        self._t = T(**kwargs)
   
    def hookCB(self, cb):
        """ hook回调函数
        """
        if cb.on_kline_update_callback:
            self._original_on_kline_update_callback = cb.on_kline_update_callback
            cb.on_kline_update_callback = self.on_kline_update_callback
        if cb.on_orderbook_update_callback:
            self._original_on_orderbook_update_callback = cb.on_orderbook_update_callback
            cb.on_orderbook_update_callback = self.on_orderbook_update_callback
        if cb.on_trade_update_callback:
            self._original_on_trade_update_callback = cb.on_trade_update_callback
            cb.on_trade_update_callback = self.on_trade_update_callback
        if cb.on_ticker_update_callback:
            self._original_on_ticker_update_callback = cb.on_ticker_update_callback
            cb.on_ticker_update_callback = self.on_ticker_update_callback
        if cb.on_order_update_callback:
            self._original_on_order_update_callback = cb.on_order_update_callback
            cb.on_order_update_callback = self.on_order_update_callback
        if cb.on_fill_update_callback:
            self._original_on_fill_update_callback = cb.on_fill_update_callback
            cb.on_fill_update_callback = self.on_fill_update_callback
        if cb.on_position_update_callback:
            self._original_on_position_update_callback = cb.on_position_update_callback
            cb.on_position_update_callback = self.on_position_update_callback
        if cb.on_asset_update_callback:
            self._original_on_asset_update_callback = cb.on_asset_update_callback
            cb.on_asset_update_callback = self.on_asset_update_callback

    async def on_kline_update_callback(self, kline: Kline):
        """ 市场K线更新
        """
        if self.native_to_system:
            kline.symbol = self.native_to_system[kline.symbol] #'交易所原始符号'转换成'量化平台通用符号'
        await self._original_on_kline_update_callback(kline)

    async def on_orderbook_update_callback(self, orderbook: Orderbook):
        """ 订单薄更新
        """
        if self.native_to_system:
            orderbook.symbol = self.native_to_system[orderbook.symbol] #'交易所原始符号'转换成'量化平台通用符号'
        await self._original_on_orderbook_update_callback(orderbook)

    async def on_trade_update_callback(self, trade: Trade):
        """ 市场最新成交更新
        """
        if self.native_to_system:
            trade.symbol = self.native_to_system[trade.symbol] #'交易所原始符号'转换成'量化平台通用符号'
        await self._original_on_trade_update_callback(trade)

    async def on_ticker_update_callback(self, ticker: Ticker):
        """ 市场行情tick更新
        """
        if self.native_to_system:
            ticker.symbol = self.native_to_system[ticker.symbol] #'交易所原始符号'转换成'量化平台通用符号'
        await self._original_on_ticker_update_callback(ticker)

    async def on_order_update_callback(self, order: Order):
        """ 订单状态更新
        """
        if self.native_to_system:
            order.symbol = self.native_to_system[order.symbol] #'交易所原始符号'转换成'量化平台通用符号'
        await self._original_on_order_update_callback(order)

    async def on_fill_update_callback(self, fill: Fill):
        """ 订单成交通知
        """
        if self.native_to_system:
            fill.symbol = self.native_to_system[fill.symbol] #'交易所原始符号'转换成'量化平台通用符号'
        await self._original_on_fill_update_callback(fill)

    async def on_position_update_callback(self, position: Position):
        """ 持仓更新
        """
        if self.native_to_system:
            position.symbol = self.native_to_system[position.symbol] #'交易所原始符号'转换成'量化平台通用符号'
        await self._original_on_position_update_callback(position)

    async def on_asset_update_callback(self, asset: Asset):
        """ 账户资产更新
        """
        if self.is_upper: #如果币种符号需要转换成大写,就进行转换
            _assets = defaultdict(lambda: {k: 0.0 for k in {'free', 'locked', 'total'}})
            for (k, v) in asset.assets.items():
                _assets[k.upper()] = v
            asset.assets = _assets
        await self._original_on_asset_update_callback(asset)

    @property
    def rest_api(self):
        return self._t.rest_api

    async def get_orders(self, symbol):
        """ 获取当前挂单列表

        Args:
            symbol: Trade target

        Returns:
            orders: Order list if successfully, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        if self.system_to_native: #映射列表不为空的情况下
            symbol = self.system_to_native.get(symbol) #'量化平台通用符号'转换成'交易所原始符号'
            if not symbol: #找不到对应符号,就返回错误
                return None, "symbol not found"
        orders, error = await self._t.get_orders(symbol)
        if not error:
            #将原生符号转换成平台通用符号
            if self.native_to_system:
                for o in orders:
                    o.symbol = self.native_to_system[o.symbol]
        return orders, error

    async def get_assets(self):
        """ 获取交易账户资产信息

        Args:
            None

        Returns:
            assets: Asset if successfully, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        asset, error = await self._t.get_assets()
        if not error:
            if self.is_upper: #币种是否转换为大写
                _assets = defaultdict(lambda: {k: 0.0 for k in {'free', 'locked', 'total'}})
                for (k, v) in asset.assets.items():
                    _assets[k.upper()] = v
                asset.assets = _assets
        return asset, error

    async def get_position(self, symbol):
        """ 获取当前持仓

        Args:
            symbol: Trade target

        Returns:
            position: Position if successfully, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        if self.system_to_native: #映射列表不为空的情况下
            symbol = self.system_to_native.get(symbol) #'量化平台通用符号'转换成'交易所原始符号'
            if not symbol: #找不到对应符号,就返回错误
                return None, "symbol not found"
        position, error = await self._t.get_position(symbol)
        if not error:
            #将原生符号转换成平台通用符号
            if self.native_to_system:
                position.symbol = self.native_to_system[position.symbol]
        return position, error

    async def get_symbol_info(self, symbol):
        """ 获取指定符号相关信息

        Args:
            symbol: Trade target

        Returns:
            symbol_info: SymbolInfo if successfully, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        if self.system_to_native: #映射列表不为空的情况下
            symbol = self.system_to_native.get(symbol) #'量化平台通用符号'转换成'交易所原始符号'
            if not symbol: #找不到对应符号,就返回错误
                return None, "symbol not found"
        symbol_info, error = await self._t.get_symbol_info(symbol)
        if not error:
            #将原生符号转换成平台通用符号
            if self.native_to_system:
                symbol_info.symbol = self.native_to_system[symbol_info.symbol]
            #币种大写
            if self.is_upper:
                symbol_info.base_currency = symbol_info.base_currency.upper()
                symbol_info.quote_currency = symbol_info.quote_currency.upper()
                symbol_info.settlement_currency = symbol_info.settlement_currency.upper()
        return symbol_info, error

    async def create_order(self, symbol, action, price, quantity, order_type=ORDER_TYPE_LIMIT, **kwargs):
        """ Create an order.

        Args:
            symbol: Trade target
            action: Trade direction, `BUY` or `SELL`.
            price: Price of each contract.
            quantity: The buying or selling quantity.
            order_type: Order type, `MARKET` or `LIMIT`.

        Returns:
            order_no: Order ID if created successfully, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        if self.system_to_native: #映射列表不为空的情况下
            symbol = self.system_to_native.get(symbol) #'量化平台通用符号'转换成'交易所原始符号'
            if not symbol: #找不到对应符号,就返回错误
                return None, "symbol not found"
        order_no, error = await self._t.create_order(symbol, action, price, quantity, order_type, **kwargs)
        return order_no, error

    async def revoke_order(self, symbol, *order_nos):
        """ Revoke (an) order(s).

        Args:
            symbol: Trade target
            order_nos: Order id list, you can set this param to 0 or multiple items. If you set 0 param, you can cancel all orders for 
            this symbol. If you set 1 or multiple param, you can cancel an or multiple order.

        备注:关于批量删除订单函数返回值格式,如果函数调用失败了那肯定是return None, error
             如果函数调用成功,但是多个订单有成功有失败的情况,比如输入3个订单id,成功2个,失败1个,那么
             返回值统一都类似: 
             return [(成功订单ID, None),(成功订单ID, None),(失败订单ID, "失败原因")], None
        """
        if self.system_to_native: #映射列表不为空的情况下
            symbol = self.system_to_native.get(symbol) #'量化平台通用符号'转换成'交易所原始符号'
            if not symbol: #找不到对应符号,就返回错误
                return None, "symbol not found"
        success, error = await self._t.revoke_order(symbol, *order_nos)
        return success, error

    async def invalid_indicate(self, symbol, indicate_type):
        """ update (an) callback function.

        Args:
            symbol: Trade target
            indicate_type: INDICATE_ORDER, INDICATE_ASSET, INDICATE_POSITION

        Returns:
            success: If execute successfully, return True, otherwise it's False.
            error: If execute failed, return error information, otherwise it's None.
        """
        if self.system_to_native: #映射列表不为空的情况下
            symbol = self.system_to_native.get(symbol) #'量化平台通用符号'转换成'交易所原始符号'
            if not symbol: #找不到对应符号,就返回错误
                return None, "symbol not found"
        success, error = await self._t.invalid_indicate(symbol, indicate_type)
        return success, error

    def shutdown(self):
        """
        """
        pass

    def csv_write(self, header, row):
        """
        """
        if hasattr(self._t, "csv_write"):
            self._t.csv_write(header, row)