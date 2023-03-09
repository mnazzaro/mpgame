from flask import request
from flask_socketio import emit, ConnectionRefusedError, disconnect
from flask_login import current_user
from model.game_manager import GameManager

import logging

from socket_blueprint import SocketBlueprint

blueprint = SocketBlueprint ('events', __name__)
logger = logging.Logger(__name__)



@blueprint.on('connect')
def connect ():
    if current_user.is_authenticated():
        # TODO
        pass
    else:
        return False
    



