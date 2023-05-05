from flask import request, make_response, Blueprint, current_app
from flask_cors import cross_origin

from ..mpgameservices.model.player import Player

import sys
sys.path.append('..')
from mplib.auth.authentication import login as auth_login
from mplib.auth.sessions.cookies import generate_cookie
# from mplib.game.authorize import authorize_player_for_table

blueprint = Blueprint('routes', __name__, '')

@blueprint.route('/login', methods=['POST'])
@cross_origin(expose_headers=['access_token'])
def login ():
    # TODO: validate form
    try:
        with current_app.app_context():
            token, session = auth_login (request.json)
    except Exception as e:
        return {"result": False}, 403 # TODO: Auth Failure 
    
    return {"result": True, "socketAddress": "http://172.17.0.1:5000"}, 200, {"access_token": token}


@blueprint.route('/add', methods=['GET'])
def add ():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    result = current_app.celery.send_task('tasks.add_together', args=[x, y])
    r = result.get()
    print (f"Processing is {r}")
    return (f"Processing is {r}")

@blueprint.route('/add_player', methods=['GET'])
def add_player ():
    id = int(request.args.get('id'))
    stack = float(request.args.get('stack'))
    result = current_app.celery.send_task('game.add_player', args=[Player(id, stack).serialize()])
    r = result.get()
    print (r)
    return r