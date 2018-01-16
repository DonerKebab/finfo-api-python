# -*- coding: utf-8 -*-
"""
    admin.api.market
    ~~~~~~~~~~~~~~~

    Market search endpoints
"""

from flask import Blueprint, current_app as app, abort

from ..core import AdminError, es, cache
from . import route, auth_required

bp = Blueprint('market', __name__, url_prefix='/market')

@route(bp, '/')
def index():
    args = {k: v for k, v in app.market_parser.parse_args().iteritems() if v is not None}
    # get filters
    filters = app.market_parser.get_market_filters(args)

    sort = [
            {"floorCode": {"order": "ASC"}},
            {"tradingDate": {"order": "DESC"}},
            {"time": {"order": "ASC"}}
        ]

    return es.filtered_search(doc_type='market', filters=filters, args=args, sort=sort)
