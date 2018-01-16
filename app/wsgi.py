# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    admin wsgi module
"""

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from admin import api as api

api_app = api.create_app()
application = DispatcherMiddleware(api_app, {})


if __name__ == '__main__':
    run_simple('0.0.0.0', 8000, application, use_reloader=True, use_debugger=True)