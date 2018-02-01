# -*- coding: utf-8 -*-
"""
    admin.api.parsers
    ~~~~~~~~~~~~~~~~~

    Query parsers
"""


from flask.ext.restful.reqparse import RequestParser
from flask import current_app as app


class MarketRequestParser(RequestParser):

    def __init__(self, *args, **kwargs):
        super(MarketRequestParser, self).__init__(*args, **kwargs)

        self.add_argument('tradingDate', type=str)  
        self.add_argument('time', type=str)
        self.add_argument('floorCode', type=str)
        self.add_argument('limit', type=int, default=2000)
        self.add_argument('_source', type=str)
        self.add_argument('page', type=int)
        self.add_argument('indexCode', type=str)

    def get_market_filters(self, args):

        filters = []

        for k, v in args.iteritems():
            if 'tradingDate' == k:
                filters.append({"term": {"tradingDate": v}})
            elif 'floorCode' == k:
                filters.append({"term": {"floorCode": v}})
            elif 'indexCode' == k:
                filters.append({"term": {"indexCode": v}})
            elif 'time' == k:
                filters.append({"term": {"time": v}})
        return filters


class DerivativeRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        super(DerivativeRequestParser, self).__init__(*args, **kwargs)

        self.add_argument('code', type=str)
        self.add_argument('tradingDate', type=str) 
        self.add_argument('time', type=str)
        self.add_argument('deriCode', type=str)
        self.add_argument('limit', type=int, default=2000)
        self.add_argument('_source', type=str)
        self.add_argument('page', type=int)

    def get_derivative_filters(self, args):

        filters = []
        for k, v in args.iteritems():
            if 'tradingDate' == k:
                filters.append({"term": {"tradingDate": v}})
            elif 'code' == k:
                filters.append({"term": {"code": v}})
            elif 'deriCode' == k:
                filters.append({"term": {"deriCode": v}})
            elif 'time' == k:
                filters.append({"term": {"time": v}})
        return filters

class StockRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        super(StockRequestParser, self).__init__(*args, **kwargs)

        self.add_argument('tradingDate', type=str)
        self.add_argument('symbol', type=str) 
        self.add_argument('floorCode', type=str)
        self.add_argument('limit', type=int, default=2000)
        self.add_argument('_source', type=str)
        self.add_argument('page', type=int)

    def get_stock_filters(self, args):

        filters = []
        for k, v in args.iteritems():
            if 'tradingDate' == k:
                filters.append({"term": {"tradingDate": v}})
            elif 'floorCode' == k:
                filters.append({"term": {"floorCode": v}})
            elif 'symbol' == k:
                # allow multi symbol requests
                or_filter = {"or": []}
                for n in str(v).split(','):
                    or_filter["or"].append({"term": {"symbol": n}})
                filters.append(or_filter)
        return filters
