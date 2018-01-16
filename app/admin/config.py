# -*- coding: utf-8 -*-

import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    SECRET_KEY = 'cezCupwob6EmivVuwerd'
    LOCALE = 'en_GB.utf8'

    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    SECURITY_CONFIRMABLE = True

    ELASTICSEARCH_PORT = 9200 
    ELASTICSEARCH_HOST = '192.168.103.141'
    ELASTICSEARCH_INDEX = 'api'

    CACHE_TIMEOUT = 60 * 60  # one hours

    
class DevelopmentConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                          'tests/data-test.sqlite')
    WTF_CSRF_ENABLED = False
    ADMIN_PASSWORD = u'pass'


class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
