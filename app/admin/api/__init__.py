# -*- coding: utf-8 -*-
from functools import wraps
import sys

from flask import jsonify, current_app as app, abort

from ..core import AdminError, cache, es
from ..helpers import lookup_url
from .parsers import MarketRequestParser,DerivativeRequestParser
from .. import factory
from flasgger import Swagger

def create_app(settings_override=None):
    app = factory.create_app(__name__, __path__, settings_override)

    # register custom error handlers
    app.errorhandler(AdminError)(on_admin_error)
    app.errorhandler(404)(on_404)
    app.errorhandler(500)(on_500)

    app.market_parser = MarketRequestParser()
    app.derivative_parser = DerivativeRequestParser()

    app.url_build_error_handlers.append(external_url_handler)

    # @app.after_request
    # def set_headers(response):        
    #     response.headers['X-Active-ES-Cluster'] = es.active_cluster
    #     return response
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

def auth_required(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):

        parsed_args = app.auth_parser.parse_args()

        token = parsed_args['token']
        if not token:
            abort(401)

        # check token already in cache
        api_cache = cache.get(token)
        if api_cache:
            return view_function(*args, **kwargs)

        else:
            try:
                client = clients.find(token=token, limit=1)

            except Exception as e:
                
                if app.sentry:
                    app.sentry.captureMessage('Authentication error, please check if tokens.c52.io is accessible')
                
                app.deal_parser.add_argument('country', type=str, default='uk')
                return view_function(*args, **kwargs)

            if client:
                app.deal_parser.add_argument('country', type=str, default=client.country)
                cache.set(token, client, app.config['CACHE_TIMEOUT'])
                return view_function(*args, **kwargs)
            else:
                abort(401)

    return decorated_function
