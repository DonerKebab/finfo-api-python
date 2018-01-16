# -*- coding: utf-8 -*-
"""
    admin.helpers
    ~~~~~~~~~~~~~

    admin helpers module
"""

import pkgutil
import importlib
import requests
import json
from flask.json import JSONEncoder as BaseJSONEncoder
from flask import Blueprint, current_app

from os.path import join

from core import es


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application found
        in all modules for the specific package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('{0}.{1}'.format(package_name, name))
        for item in dir(m):
            item = getattr(m, item)

            if isinstance(item, Blueprint):

                app.register_blueprint(item)
            rv.append(item)
    return rv


def lookup_url(endpoint, values):
    print u'endpoint: {} with values {}'.format(endpoint, values)
    if 'images.view_image' == endpoint:
        return '/images/{}'.format(values['filename'])
    return None


