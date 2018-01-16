# -*- coding: utf-8 -*-
"""
    admin.api.market
    ~~~~~~~~~~~~~~~

    Market search endpoints
"""

from flask import Blueprint, current_app as app, abort

from ..core import AdminError, es, cache
from . import route, auth_required

bp = Blueprint('derivative', __name__, url_prefix='/derivative')

@route(bp, '/')
def index():
    args = {k: v for k, v in app.derivative_parser.parse_args().iteritems() if v is not None}

    # get filters
    filters = app.derivative_parser.get_derivative_filters(args)
    
    sort = [
            {"code": {"order": "ASC"}},
            {"tradingDate": {"order": "DESC"}},
            {"time": {"order": "ASC"}}
        ]

    return es.filtered_search(doc_type='derivative', filters=filters, args=args, sort=sort)
