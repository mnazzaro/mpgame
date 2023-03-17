from typing import Callable

from flask import request
from flask_socketio import emit, ConnectionRefusedError, disconnect
from flask_login import current_user
# from model.game_manager import GameManager

from functools import wraps

import logging

from Controller.socket_blueprint import SocketBlueprint

blueprint = SocketBlueprint ('events', __name__)
logger = logging.Logger(__name__)

def login_required (func: Callable) -> Callable:

    @wraps(func)
    def wrapped (*args, **kwargs):
        if current_user.is_authenticated():
            return func(*args, **kwargs)
        disconnect()

    return wrapped


@blueprint.on('connect')
@login_required
def connect ():
    print ("Authorized user connected!")
    



