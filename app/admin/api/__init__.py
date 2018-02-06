# -*- coding: utf-8 -*-
from functools import wraps
import sys

from flask import jsonify, current_app as app, abort, after_this_request, request
from flasgger import Swagger
from cStringIO import StringIO as IO
import gzip

from ..core import AdminError, cache, es
from ..helpers import lookup_url
from .parsers import MarketRequestParser, DerivativeRequestParser, StockRequestParser, TradeRequestParser
from .. import factory



def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    # register custom error handlers
    app.errorhandler(AdminError)(on_admin_error)
    app.errorhandler(404)(on_404)
    app.errorhandler(500)(on_500)

    app.market_parser = MarketRequestParser()
    app.derivative_parser = DerivativeRequestParser()
    app.stock_parser = StockRequestParser()
    app.trade_parser = TradeRequestParser()

    app.url_build_error_handlers.append(external_url_handler)

    app.config['SWAGGER'] = {
    'title': 'Finfo API'
    }
    swagger = Swagger(app)
    return app


def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            sc = 200
            rv = f(*args, **kwargs)
            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return jsonify(dict(data=rv)), sc
        return f

    return decorator


def on_admin_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_404(e):
    return jsonify(dict(error=u'Not found')), 404


def on_500(e):
    print(str(e))


def external_url_handler(error, endpoint, values):
    """Looks up an external URL when `url_for` cannot build a URL."""
    print(u'external_url_handler() called')
    url = lookup_url(endpoint, values)
    if url is None:
        # External lookup did not have a URL.
        # Re-raise the BuildError, in context of original traceback.
        exc_type, exc_value, tb = sys.exc_info()
        if exc_value is error:
            raise exc_type, exc_value, tb
        else:
            raise error
    # url_for will use this result, instead of raising BuildError.
    return url


def gzipped(f):
    @wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            # accept_encoding = request.headers.get('Accept-Encoding', '')

            # if 'gzip' not in accept_encoding.lower():
            #     return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >= 300 or
                'Content-Encoding' in response.headers):
                return response
            gzip_buffer = IO()
            with  gzip.GzipFile(mode='wb', fileobj=gzip_buffer) as  gzip_file:
                gzip_file.write(response.data.replace(' ', ''))

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func