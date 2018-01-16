# -*- coding: utf-8 -*-
"""
    admin.api.parsers
    ~~~~~~~~~~~~~~~~~

    Query parsers
"""

from flask.ext.restful.reqparse import RequestParser
from flask import current_app as app
import datetime


class MarketRequestParser(RequestParser):

    def __init__(self, *args, **kwargs):
        super(MarketRequestParser, self).__init__(*args, **kwargs)

        self.add_argument('tradingDate', type=str)  
        self.add_argument('time', type=str)
        self.add_argument('floorCode', type=str)
        self.add_argument('limit', type=int, default=2000)
        self.add_argument('_source', type=str)

    def get_market_filters(self, args):

        filters = []

        for k, v in args.iteritems():
            # contract
            if 'tradingDate' == k:
                filters.append({"term": {"tradingDate": v}})
            elif 'floorCode' == k:
                filters.append({"term": {"floorCode": v}})

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

    def get_derivative_filters(self, args):

        filters = []
        for k, v in args.iteritems():
            if 'tradingDate' == k:
                filters.append({"term": {"tradingDate": v}})
            elif 'code' == k:
                filters.append({"term": {"code": v}})
            elif 'deriCode' == k:
                filters.append({"term": {"deriCode": v}})
        return filters
