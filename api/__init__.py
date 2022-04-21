__version__ = '0.1.0'
import os
from flask import Flask
# use gunicorn to run api

from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    # initialize the database
    from . import postgres
    postgres.init_db()

    # register blueprints
    from . import api
    app.register_blueprint(api.url_api)

    return app    

api=create_app()