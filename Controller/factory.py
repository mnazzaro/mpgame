from flask import Flask
from flask_socketio import SocketIO

import sys
sys.path.append('..')
from ..CeleryProcesses.celery_factory import create_celery

sys.path.append('../..')
from mplib.auth import Auth

from .events import blueprint as events_bp
from .routes import blueprint as routes_bp

def create_app(config_path: str = None) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(
        config_path if config_path \
        else 'config.py'
    )

    print (app.config['SERVICE_TYPE_FOR_AUTH'])

    Auth(app)

    sio = SocketIO(app)

    app.register_blueprint(events_bp)
    app.register_blueprint(routes_bp)

    celery = create_celery(app)
    app.celery = celery

    return app