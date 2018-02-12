# -*- coding: utf-8 -*-
"""
    admin.api.stock
    ~~~~~~~~~~~~~~~

    Stock search endpoints
"""

from flask import Blueprint, current_app as app, abort
import datetime
from datetime import timedelta

from ..core import AdminError, es, cache
from . import route, gzipped

bp = Blueprint('stocks', __name__, url_prefix='/stocks')

@route(bp, '/intraday')
@gzipped
def index():
    """List all intraday stock.
    ---
    parameters:
      - name: symbol
        in: path
        type: string
        required: false
      - name: tradingDate
        in: path
        type: string
        required: false 
      - name: floorCode
        in: path
        type: string
        required: false 
      - name: page
        in: path
        type: integer
        default: 1
        required: false
      - name: limit
        in: path
        type: integer
        default: 2000
        required: false
    definitions:
      stock:
        type: object
        properties:
          floorCode:
            type: string
          tradingDate:
            type: string
          time:
            type: string
          symbol:
            type: string
          lastVol:
            type: double
    responses:
      200:
        description: A list of stock
        schema:
          $ref: '#/definitions/stock'

    """
    args = {k: v for k, v in app.stock_parser.parse_args().iteritems() if v is not None}
    if args.get('tradingDate') is None:
        args['tradingDate'] = datetime.datetime.today().strftime('%Y-%m-%d')
    # get filters
    filters = app.stock_parser.get_stock_filters(args)

    sort = [
            {"symbol": {"order": "ASC"}},
            {"tradingDate": {"order": "DESC"}},
            {args.get('sortBy', 'time'): {"order": args.get('sortType', 'ASC')}}
        ]


    return es.filtered_search(doc_type='stock', filters=filters, args=args, sort=sort)


@route(bp, '/intraday/history')
@gzipped
def history():
    """List all history stock.
    ---
    parameters:
      - name: symbol
        in: path
        type: string
        required: false
      - name: tradingDate
        in: path
        type: string
        required: false 
      - name: floorCode
        in: path
        type: string
        required: false 
      - name: page
        in: path
        type: integer
        default: 1
        required: false
      - name: limit
        in: path
        type: integer
        default: 2000
        required: false
    definitions:
      stock:
        type: object
        properties:
          floorCode:
            type: string
          tradingDate:
            type: string
          time:
            type: string
          symbol:
            type: string
          lastVol:
            type: double
    responses:
      200:
        description: A list of stock
        schema:
          $ref: '#/definitions/stock'

    """
    args = {k: v for k, v in app.stock_parser.parse_args().iteritems() if v is not None}
    if args.get('tradingDate') is None:
        yesterday = datetime.datetime.today() - timedelta(days=1)
        args['tradingDate'] = yesterday.strftime('%Y-%m-%d')
    # get filters
    filters = app.stock_parser.get_stock_filters(args)

    sort = [
            {"symbol": {"order": "ASC"}},
            {"tradingDate": {"order": "DESC"}},
            {args.get('sortBy', 'time'): {"order": args.get('sortType', 'ASC')}}
        ]


    return es.filtered_search(doc_type='stock', filters=filters, args=args, sort=sort)

