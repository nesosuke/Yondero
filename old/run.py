import os
from flask import Flask
# from flask_login import LoginManager
# use gunicorn to run api

from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__,)
    CORS(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # initialize the database
    from backend import postgres
    postgres.init_db()

    # register blueprints
    from backend import api
    app.register_blueprint(api.bp)

    from frontend import web
    app.register_blueprint(web.bp)

    # # initialize the login manager  #TODO
    # login_manager = LoginManager()
    # login_manager.init_app(app)

    return app


app = create_app()
