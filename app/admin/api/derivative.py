# -*- coding: utf-8 -*-
"""
    admin.api.market
    ~~~~~~~~~~~~~~~

    Market search endpoints
"""

from flask import Blueprint, current_app as app, abort

from ..core import AdminError, es, cache
from . import route, auth_required

bp = Blueprint('trade', __name__, url_prefix='/trade')

@route(bp, '/derivatives/intraday')
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

    # get filters
    filters = app.derivative_parser.get_derivative_filters(args)
    
    sort = [
            {"code": {"order": "ASC"}},
            {"tradingDate": {"order": "DESC"}},
            {"time": {"order": "ASC"}}
        ]

    return es.filtered_search(doc_type='derivative', filters=filters, args=args, sort=sort)
