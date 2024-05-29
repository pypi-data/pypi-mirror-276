# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheByTimestamp
from ccxt.base.types import Int, OrderBook, Ticker, Trade
from ccxt.async_support.base.ws.client import Client
from typing import List
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import BadRequest


class p2b(ccxt.async_support.p2b):

    def describe(self):
        return self.deep_extend(super(p2b, self).describe(), {
            'has': {
                'ws': True,
                'cancelAllOrdersWs': False,
                'cancelOrdersWs': False,
                'cancelOrderWs': False,
                'createOrderWs': False,
                'editOrderWs': False,
                'fetchBalanceWs': False,
                'fetchOpenOrdersWs': False,
                'fetchOrderWs': False,
                'fetchTradesWs': False,
                'watchBalance': False,
                'watchMyTrades': False,
                'watchOHLCV': True,
                'watchOrderBook': True,
                'watchOrders': False,
                # 'watchStatus': True,
                'watchTicker': True,
                'watchTickers': False,  # in the docs but does not return anything when subscribed to
                'watchTrades': True,
            },
            'urls': {
                'api': {
                    'ws': 'wss://apiws.p2pb2b.com/',
                },
            },
            'options': {
                'OHLCVLimit': 1000,
                'tradesLimit': 1000,
                'timeframes': {
                    '15m': 900,
                    '30m': 1800,
                    '1h': 3600,
                    '1d': 86400,
                },
                'watchTicker': {
                    'name': 'state',  # or 'price'
                },
                'watchTickers': {
                    'name': 'state',  # or 'price'
                },
                'tickerSubs': self.create_safe_dictionary(),
            },
            'streaming': {
                'ping': self.ping,
            },
        })

    async def subscribe(self, name: str, messageHash: str, request, params={}):
        """
         * @ignore
        Connects to a websocket channel
        :param str name: name of the channel
        :param str messageHash: string to look up in handler
        :param str[]|float[] request: endpoint parameters
        :param dict [params]: extra parameters specific to the p2b api
        :returns dict: data from the websocket stream
        """
        url = self.urls['api']['ws']
        subscribe: dict = {
            'method': name,
            'params': request,
            'id': self.milliseconds(),
        }
        query = self.extend(subscribe, params)
        return await self.watch(url, messageHash, query, messageHash)

    async def watch_ohlcv(self, symbol: str, timeframe='15m', since: Int = None, limit: Int = None, params={}) -> List[list]:
        """
        watches historical candlestick data containing the open, high, low, and close price, and the volume of a market. Can only subscribe to one timeframe at a time for each symbol
        :see: https://github.com/P2B-team/P2B-WSS-Public/blob/main/wss_documentation.md#kline-candlestick
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: 15m, 30m, 1h or 1d
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        await self.load_markets()
        timeframes = self.safe_value(self.options, 'timeframes', {})
        channel = self.safe_integer(timeframes, timeframe)
        if channel is None:
            raise BadRequest(self.id + ' watchOHLCV cannot take a timeframe of ' + timeframe)
        market = self.market(symbol)
        request = [
            market['id'],
            channel,
        ]
        messageHash = 'kline::' + market['symbol']
        ohlcv = await self.subscribe('kline.subscribe', messageHash, request, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    async def watch_ticker(self, symbol: str, params={}) -> Ticker:
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :see: https://github.com/P2B-team/P2B-WSS-Public/blob/main/wss_documentation.md#last-price
        :see: https://github.com/P2B-team/P2B-WSS-Public/blob/main/wss_documentation.md#market-status
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param dict [params.method]: 'state'(default) or 'price'
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        watchTickerOptions = self.safe_dict(self.options, 'watchTicker')
        name = self.safe_string(watchTickerOptions, 'name', 'state')  # or price
        name, params = self.handle_option_and_params(params, 'method', 'name', name)
        market = self.market(symbol)
        symbol = market['symbol']
        self.options['tickerSubs'][market['id']] = True  # we need to re-subscribe to all tickers upon watching a new ticker
        tickerSubs = self.options['tickerSubs']
        request = list(tickerSubs.keys())
        messageHash = name + '::' + market['symbol']
        return await self.subscribe(name + '.subscribe', messageHash, request, params)

    async def watch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        get the list of most recent trades for a particular symbol
        :see: https://github.com/P2B-team/P2B-WSS-Public/blob/main/wss_documentation.md#deals
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `trade structures <https://docs.ccxt.com/#/?id=public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = [
            market['id'],
        ]
        messageHash = 'deals::' + market['symbol']
        trades = await self.subscribe('deals.subscribe', messageHash, request, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    async def watch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :see: https://github.com/P2B-team/P2B-WSS-Public/blob/main/wss_documentation.md#depth-of-market
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: 1-100, default=100
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param float [params.interval]: 0, 0.00000001, 0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, interval of precision for order, default=0.001
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        name = 'depth.subscribe'
        messageHash = 'orderbook::' + market['symbol']
        interval = self.safe_string(params, 'interval', '0.001')
        if limit is None:
            limit = 100
        request = [
            market['id'],
            limit,
            interval,
        ]
        orderbook = await self.subscribe(name, messageHash, request, params)
        return orderbook.limit()

    def handle_ohlcv(self, client: Client, message):
        #
        #    {
        #        "method": "kline.update",
        #        "params": [
        #            [
        #                1657648800,             # Kline start time
        #                "0.054146",             # Kline open price
        #                "0.053938",             # Kline close price(current price)
        #                "0.054146",             # Kline high price
        #                "0.053911",             # Kline low price
        #                "596.4674",             # Volume for stock currency
        #                "32.2298758767",        # Volume for money currency
        #                "ETH_BTC"               # Market
        #            ]
        #        ],
        #        "id": null
        #    }
        #
        data = self.safe_list(message, 'params')
        data = self.safe_list(data, 0)
        method = self.safe_string(message, 'method')
        splitMethod = method.split('.')
        channel = self.safe_string(splitMethod, 0)
        marketId = self.safe_string(data, 7)
        market = self.safe_market(marketId)
        timeframes = self.safe_dict(self.options, 'timeframes', {})
        timeframe = self.find_timeframe(channel, timeframes)
        symbol = self.safe_string(market, 'symbol')
        messageHash = channel + '::' + symbol
        parsed = self.parse_ohlcv(data, market)
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if symbol is not None:
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCacheByTimestamp(limit)
                self.ohlcvs[symbol][timeframe] = stored
            stored.append(parsed)
            client.resolve(stored, messageHash)
        return message

    def handle_trade(self, client: Client, message):
        #
        #    {
        #        "method": "deals.update",
        #        "params": [
        #            "ETH_BTC",
        #            [
        #                {
        #                    "id": 4503032979,               # Order_id
        #                    "amount": "0.103",
        #                    "type": "sell",                 # Side
        #                    "time": 1657661950.8487639,     # Creation time
        #                    "price": "0.05361"
        #                },
        #                ...
        #            ]
        #        ],
        #        "id": null
        #    }
        #
        data = self.safe_list(message, 'params', [])
        trades = self.safe_list(data, 1)
        marketId = self.safe_string(data, 0)
        market = self.safe_market(marketId)
        symbol = self.safe_string(market, 'symbol')
        tradesArray = self.safe_value(self.trades, symbol)
        if tradesArray is None:
            tradesLimit = self.safe_integer(self.options, 'tradesLimit', 1000)
            tradesArray = ArrayCache(tradesLimit)
            self.trades[symbol] = tradesArray
        for i in range(0, len(trades)):
            item = trades[i]
            trade = self.parse_trade(item, market)
            tradesArray.append(trade)
        messageHash = 'deals::' + symbol
        client.resolve(tradesArray, messageHash)
        return message

    def handle_ticker(self, client: Client, message):
        #
        # state
        #
        #    {
        #        "method": "state.update",
        #        "params": [
        #            "ETH_BTC",
        #            {
        #                "high": "0.055774",         # High price for the last 24h
        #                "close": "0.053679",        # Close price for the last 24h
        #                "low": "0.053462",          # Low price for the last 24h
        #                "period": 86400,            # Period 24h
        #                "last": "0.053679",         # Last price for the last 24h
        #                "volume": "38463.6132",     # Stock volume for the last 24h
        #                "open": "0.055682",         # Open price for the last 24h
        #                "deal": "2091.0038055314"   # Money volume for the last 24h
        #            }
        #        ],
        #        "id": null
        #    }
        #
        # price
        #
        #    {
        #        "method": "price.update",
        #        "params": [
        #            "ETH_BTC",      # market
        #            "0.053836"      # last price
        #        ],
        #        "id": null
        #    }
        #
        data = self.safe_list(message, 'params', [])
        marketId = self.safe_string(data, 0)
        market = self.safe_market(marketId)
        method = self.safe_string(message, 'method')
        splitMethod = method.split('.')
        messageHashStart = self.safe_string(splitMethod, 0)
        tickerData = self.safe_dict(data, 1)
        ticker = None
        if method == 'price.update':
            lastPrice = self.safe_string(data, 1)
            ticker = self.safe_ticker({
                'last': lastPrice,
                'close': lastPrice,
                'symbol': market['symbol'],
            })
        else:
            ticker = self.parse_ticker(tickerData, market)
        symbol = ticker['symbol']
        messageHash = messageHashStart + '::' + symbol
        client.resolve(ticker, messageHash)
        return message

    def handle_order_book(self, client: Client, message):
        #
        #    {
        #        "method": "depth.update",
        #        "params": [
        #            False,                          # True - all records, False - new records
        #            {
        #                "asks": [                  # side
        #                    [
        #                        "19509.81",         # price
        #                        "0.277"             # amount
        #                    ]
        #                ]
        #            },
        #            "BTC_USDT"
        #        ],
        #        "id": null
        #    }
        #
        params = self.safe_list(message, 'params', [])
        data = self.safe_dict(params, 1)
        asks = self.safe_list(data, 'asks')
        bids = self.safe_list(data, 'bids')
        marketId = self.safe_string(params, 2)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        messageHash = 'orderbook::' + market['symbol']
        subscription = self.safe_value(client.subscriptions, messageHash, {})
        limit = self.safe_integer(subscription, 'limit')
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            self.orderbooks[symbol] = self.order_book({}, limit)
            orderbook = self.orderbooks[symbol]
        if bids is not None:
            for i in range(0, len(bids)):
                bid = self.safe_value(bids, i)
                price = self.safe_number(bid, 0)
                amount = self.safe_number(bid, 1)
                bookSide = orderbook['bids']
                bookSide.store(price, amount)
        if asks is not None:
            for i in range(0, len(asks)):
                ask = self.safe_value(asks, i)
                price = self.safe_number(ask, 0)
                amount = self.safe_number(ask, 1)
                bookside = orderbook['asks']
                bookside.store(price, amount)
        orderbook['symbol'] = symbol
        client.resolve(orderbook, messageHash)

    def handle_message(self, client: Client, message):
        if self.handle_error_message(client, message):
            return
        result = self.safe_string(message, 'result')
        if result == 'pong':
            self.handle_pong(client, message)
            return
        method = self.safe_string(message, 'method')
        methods: dict = {
            'depth.update': self.handle_order_book,
            'price.update': self.handle_ticker,
            'kline.update': self.handle_ohlcv,
            'state.update': self.handle_ticker,
            'deals.update': self.handle_trade,
        }
        endpoint = self.safe_value(methods, method)
        if endpoint is not None:
            endpoint(client, message)

    def handle_error_message(self, client: Client, message):
        error = self.safe_string(message, 'error')
        if error is not None:
            raise ExchangeError(self.id + ' error: ' + self.json(error))
        return False

    def ping(self, client):
        """
        :see: https://github.com/P2B-team/P2B-WSS-Public/blob/main/wss_documentation.md#ping
         * @param client
        """
        return {
            'method': 'server.ping',
            'params': [],
            'id': self.milliseconds(),
        }

    def handle_pong(self, client: Client, message):
        #
        #    {
        #        error: null,
        #        result: 'pong',
        #        id: 1706539608030
        #    }
        #
        client.lastPong = self.safe_integer(message, 'id')
        return message

    def on_error(self, client: Client, error):
        self.options['tickerSubs'] = self.create_safe_dictionary()
        self.on_error(client, error)

    def on_close(self, client: Client, error):
        self.options['tickerSubs'] = self.create_safe_dictionary()
        self.on_close(client, error)
