# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~

    admin wsgi module
"""

from admin import api
import logging

app = api.create_app()
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run()
