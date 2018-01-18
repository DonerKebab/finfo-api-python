# -*- coding: utf-8 -*-
"""
admin.api.health
~~~~~~~~~~~~~~~~~~

health endpoint
"""

from flask import Blueprint, current_app as app, jsonify
from . import route

bp = Blueprint('health', __name__, url_prefix='/health')

@route(bp, '/')
def index():
    """Health check"""
    return {}, 200
