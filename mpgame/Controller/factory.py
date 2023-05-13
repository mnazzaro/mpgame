from typing import Tuple

from flask import Flask
from flask_socketio import SocketIO


from ..CeleryProcesses.celery_factory import create_celery

from mplib.auth import Auth
from mplib.auth.middlewares.token_auth_middleware import TokenAuthMiddleware
from mplib.model.util import create_all, drop_all
from mplib.base import wrap

from .events import blueprint as events_bp
from .routes import blueprint as routes_bp


def create_app(config_path: str = None) -> Tuple[SocketIO, Flask]:
    app = Flask(__name__)
    app.config.from_pyfile(
        config_path if config_path
        else 'config.py'
    )

    print(app.config['SERVICE_TYPE_FOR_AUTH'])

    Auth(app)

    sio = SocketIO(
        app,
        cors_allowed_origins=["http://127.0.0.1:3000", "http://127.0.0.1:5000", "http://localhost:3000"], # TODO: Sec Vuln
        message_queue=app.config.get('REDIS_URI'),
    )  # TODO: This will not fly in prod. Should be okay for now because we will work on that logic in the pairing service later

    app.register_blueprint(events_bp)
    app.register_blueprint(routes_bp)

    celery = create_celery(app)
    app.celery = celery

    # wrap(app, [TokenAuthMiddleware])

    if app.config.get('CREATE_DB'):
        with app.app_context():
            create_all()

    return sio, app
