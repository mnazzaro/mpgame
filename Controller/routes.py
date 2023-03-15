from flask import request, Blueprint, current_app

import sys
sys.path.append('..')
from mpgameservices.model.player import Player

blueprint = Blueprint('routes', __name__, '')

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