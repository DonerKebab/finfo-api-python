# -*- coding: utf-8 -*-
"""
    admin.core
    ~~~~~~~~~~

    core module
"""

from search import ElasticSearch
from werkzeug.contrib.cache import SimpleCache
from flask import current_app as app

#: Elastic search instance
es = ElasticSearch()

#: Werkzeug simple cache instance
cache = SimpleCache()


class AdminError(Exception):
    """Base application error class"""

    def __init__(self, msg):
        self.msg = msg


class AdminFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors