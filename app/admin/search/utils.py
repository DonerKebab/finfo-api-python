# -*- coding: utf-8 -*-


def get_config(app):
    items = app.config.items()
    prefix = 'ELASTICSEARCH_'

    def strip_prefix(tup):
        return tup[0].replace('ELASTICSEARCH_', ''), tup[1]

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])