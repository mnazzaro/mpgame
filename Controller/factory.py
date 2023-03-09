from flask import Flask
from socketio import SocketIO

import events

def create_app(config_path: str = None) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(
        config_path if config_path \
        else 'config.py'
    )

    sio = SocketIO(app)

    # Will have middlewares, auth, etc. later

    app.register_blueprint(events.blueprint)

    return app