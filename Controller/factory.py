from flask import Flask
from flask_socketio import SocketIO

import sys
sys.path.append('..')
from CeleryProcesses.celery_factory import create_celery

import Controller.events as events
import Controller.routes as routes

def create_app(config_path: str = None) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(
        config_path if config_path \
        else 'config.py'
    )

    sio = SocketIO(app)

    # Will have middlewares, auth, etc. later

    app.register_blueprint(events.blueprint)
    app.register_blueprint(routes.blueprint)

    celery = create_celery(app)
    app.celery = celery

    return app