# -*- coding: utf-8 -*-
"""
    admin.api.market
    ~~~~~~~~~~~~~~~

    Market search endpoints
"""

from flask import Blueprint, current_app as app, abort
import datetime

from ..core import AdminError, es, cache
from . import route, gzipped

bp = Blueprint('trade', __name__, url_prefix='/trade')

@route(bp, '/derivatives/intraday')
@gzipped
def index():
    """List all derivative.
    ---
    parameters:
      - name: code
        in: path
        type: string
        required: false
      - name: tradingDate
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
      derivative:
        type: object
        properties:
          floorCode:
            type: string
          tradingDate:
            type: string
          time:
            type: string

    responses:
      200:
        description: A list of derivative
        schema:
          $ref: '#/definitions/derivative'

    """
    args = {k: v for k, v in app.derivative_parser.parse_args().iteritems() if v is not None}
    if args.get('tradingDate') is None:
        args['tradingDate'] = datetime.datetime.today().strftime('%Y-%m-%d')
    # get filters
    filters = app.derivative_parser.get_derivative_filters(args)
    
    sort = [
            {"code": {"order": "ASC"}},
            {"tradingDate": {"order": "DESC"}},
            {args.get('sortBy', 'time'): {"order": args.get('sortType', 'ASC')}}
        ]

    return es.filtered_search(doc_type='deri', filters=filters, args=args, sort=sort)


@route(bp, '/supplyDemand')
@gzipped
def supplyDemand():
    """List all trade supply demand.
    ---
    parameters:
      - name: symbols
        in: path
        type: string
        required: false
      - name: fromDate
        in: path
        type: string
        required: false 
      - name: toDate
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
      trade:
        type: object
        properties:
          symbol:
            type: string
          tradingDate:
            type: string
          time:
            type: string

    responses:
      200:
        description: A list of trade
        schema:
          $ref: '#/definitions/trade'

    """
    args = {k: v for k, v in app.trade_parser.parse_args().iteritems() if v is not None}
    if args.get('fromDate') is None and args.get('toDate') is None :
        args['fromDate'] = datetime.datetime.today().strftime('%Y-%m-%d')

    # sorting
    sort = [
            {"symbol": {"order": "ASC"}},
            {"tradingDate": {"order": "DESC"}},
            {args.get('sortBy', 'time'): {"order": args.get('sortType', 'DESC')}}
        ]
    
    # get filters
    filters = app.trade_parser.get_trade_filters(args)
    


    return es.filtered_search(doc_type='trade', filters=filters, args=args, sort=sort)
