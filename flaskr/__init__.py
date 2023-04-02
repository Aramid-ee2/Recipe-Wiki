from flaskr import backend, pages
from flask import Flask, session
from google.cloud import storage
from flask_login import LoginManager, login_user
from flaskr.login import User
from flask_session import Session

import logging

logging.basicConfig(level=logging.DEBUG)

#creating login manager class to enable the app and flask login to work together

login_manager = LoginManager()


# The flask terminal command inside "run-flask.sh" searches for
# this method inside of __init__.py (containing flaskr module
# properties) as we set "FLASK_APP=flaskr" before running "flask".
def create_app(test_config=None, backend_instance=None):
    # Create and configure the app.
    app = Flask(
        __name__,
        instance_relative_config=True,
    )
    # Create backend class
    if backend_instance is None:
        backend_instance = backend.Backend(storage.Client())
    # This is the default secret key used for login sessions
    # By default the dev environment uses the key 'dev'
    app.config.from_mapping(SECRET_KEY='dev', SESSION_TYPE = 'filesystem')

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        # This file is not committed. Place it in production deployments.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # TODO(Project 1): Make additional modifications here for logging in, backends
    # and additional endpoints.
    pages.make_endpoints(app, backend_instance, logging)

    login_manager.init_app(app)
    #configuring the application for login
    Session(app)
    return app


#using the user_loader class to reload user object from user id
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
