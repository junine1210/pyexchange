from exchange.errors import *
from exchange.ticker import Ticker
from exchange.orderbook import *
from exchange.currency_pair import CurrencyPair
from exchange.exchange_base import ExchangeBase
from exchange.binance.binance import Binance


class ExchangeBianace(ExchangeBase):
    """
    Binance
    """
    NAME = 'Binance'
    VERSION = '1.0'
    URL = 'https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md'

    def __init__(self):
        super().__init__(self.NAME, self.VERSION, self.URL)
        self.binance = Binance()

    def get_currency_pairs(self):
        '''
        Gets currency list supported by exchange
        :return: supported currency pair list
        :rtype: CurrencyPair[]
        '''
        currency_pairs = []
        exchange_info = self.binance.get_exchange_info()
        for symbol in exchange_info['symbols']:
            base_currency = symbol['baseAsset']
            currency = symbol['symbol'][len(base_currency):]
            currency_pairs.append(CurrencyPair(base_currency, currency))
        return currency_pairs

    def get_ticker(self, currency_pair):
        '''
        Gets last price
        :param CurrencyPair currency_pair: currency pair
        :return: ticker
        :rtype: Ticker
        '''
        if currency_pair is None:
            raise InvalidParamException('currency_pair is None')
        base_currency = currency_pair.base_currency
        currency = currency_pair.currency
        symbol = base_currency + currency

        timestamp = self.binance.get_time()['serverTime']
        price = float(self.binance.get_ticker_price(symbol)['price'])
        return Ticker(currency_pair, price, timestamp)

    def get_orderbook(self, currency_pair):
        '''
        Gets orderbook information
        :param CurrencyPair currency_pair: currency pair
        :return: orderbook
        :rtype: Orderbook
        '''
        if currency_pair is None:
            raise InvalidParamException('currency_pair is None')
        base_currency = currency_pair.base_currency
        currency = currency_pair.currency
        symbol = base_currency + currency

        timestamp = self.binance.get_time()['serverTime']

        orderbook = self.binance.get_orderbook(symbol)
        asks = []
        for unit in orderbook['asks']:
            price = float(unit[0])
            amount = float(unit[1])
            asks.append(OrderbookItem(price, amount))

        bids = []
        for unit in orderbook['bids']:
            price = float(unit[0])
            amount = float(unit[1])
            asks.append(OrderbookItem(price, amount))

        return Orderbook(currency_pair, asks, bids, timestamp)
