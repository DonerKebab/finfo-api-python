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

bp = Blueprint('index', __name__, url_prefix='/index')

@route(bp, '/securities/vnmarket/intraday')
@gzipped
def index():
    """List all market.
    ---
    parameters:
      - name: floorCode
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
      market:
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
        description: A list of market
        schema:
          $ref: '#/definitions/market'

    """
    args = {k: v for k, v in app.market_parser.parse_args().iteritems() if v is not None}
    if args.get('tradingDate') is None:
        args['tradingDate'] = datetime.datetime.today().strftime('%Y-%m-%d')
    # get filters
    filters = app.market_parser.get_market_filters(args)

    sort = [
            {"floorCode": {"order": "asc"}},
            {args.get('sortBy', 'time'): args.get('sortType', 'asc').lower()}
        ]


    return es.filtered_search(doc_type='market', filters=filters, args=args, sort=sort)
