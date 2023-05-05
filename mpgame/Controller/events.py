from typing import Callable

from flask import request, current_app
from flask_socketio import emit, ConnectionRefusedError, disconnect
from flask_login import current_user
from flask_cors import cross_origin
# from model.game_manager import GameManager

from functools import wraps

import logging

from .socket_blueprint import SocketBlueprint

from mplib.auth.authenticate import authenticate_token
from mplib.auth.exceptions import MalformedTokenError, \
    AuthenticationFailureError, ExpiredTokenError
from mplib.game.authorize import authorize_player_for_table
from mplib.model.domain import Session

from ..mpgameservices.model.player import Player

import requests

blueprint = SocketBlueprint ('events', __name__)
logger = logging.Logger(__name__)

def login_required (func: Callable) -> Callable:

    @wraps(func)
    def wrapped (*args, **kwargs):
        with current_app.app_context():
            print (current_user.is_authenticated())
            if current_user.is_authenticated():
                return func(*args, **kwargs)
            disconnect()

    return wrapped

def _get_game_id () -> int:
    # TODO: This will get solved with pairing service
    return 1


@blueprint.on('connect')
def connect (auth, data):
    print ("OK CONNECT GETS CALLED")
    if auth is not None and \
        auth.get('token') is not None:
        try:
            session: Session = authenticate_token(auth.token, current_app.config.get('JWT_SECRET'))
            if not authorize_player_for_table(session.user.user_id, _get_game_id()):
                raise AuthenticationFailureError(f"Player {session.user.user_id} not authorized for table {_get_game_id()}")
        except ExpiredTokenError as e:
            # TODO: Issue request for refresh or something
            raise ConnectionRefusedError from e
        except AuthenticationFailureError as e:
            raise ConnectionRefusedError from e
        except ValueError as e:
            raise ConnectionRefusedError from e
        except Exception as e:
            raise ConnectionRefusedError from e
    else:
        raise ConnectionRefusedError ('No auth data passed')
    
    if data.get('stack') is not None:
        result = current_app.celery.send_task('game.add_player', args=[Player(session.user.user_id, data['stack']).serialize()])
    else:
        raise ConnectionRefusedError ('No stack information provided')
    
    # TODO: Return figure out return scheme for events
    players = result.get()

    

    # TODO:
    #   1. Authorize user for table *
    #   2. Send add_player event to celery *
    #   3. Send back loading data- Auth was successful, but we won't have table data until celery is done 
    #   4. Write callback for celery add_player (emit table data to client)
    #   5. Break this out into separate functions... This should not be one huge function




    



