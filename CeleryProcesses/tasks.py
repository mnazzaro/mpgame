from celery import shared_task
from celery.signals import worker_process_init, worker_process_shutdown
from flask_socketio import SocketIO
import celeryconfig
import sys
sys.path.append('..')
# TODO: This is a temporary fix because starting celery from a different directory will either
#       make mplib two levels up, or the local same dir references missing if started from one up
sys.path.append('../..')
from mpgameservices.model.game_manager import deserialize_hand
from mpgameservices.model import hand, player
from mplib.mem_store import MemoryStore

import json

import functools
from typing import Callable, Dict

# redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
redis = MemoryStore(
    host='127.0.0.1',
    port=6379
)

sio = SocketIO(message_queue=celeryconfig.broker_url)

# @worker_process_init.connect
# def init_worker(**kwargs):
#     # global db_conn
#     print('Initializing database connection for worker.')

# @worker_process_shutdown.disconnect
# def shutdown_worker(**kwargs):
#     # global db_conn
#     # if db_conn:
#     #     print('Closing database connectionn for worker.')
#     #     db_conn.close()
#     print ("Worker finished!")

# TODO: Need to handle edge cases

@shared_task(name="tasks.add_together")
def add_together (x, y):
    return x + y

# TODO: Must be specific to game_id
@shared_task(name="game.add_player")
def add_player (player: Dict):
    if redis.exists('players'):
        players = redis.read_json_as_dict('players')
        players['players'].append(player)
        redis.write_dict_as_json('players', players)
    else:
        redis.write_dict_as_json('players', {'players' : [player]})
    print ("Got to emit")
    sio.emit('load_initial_data', players['players'])



# @shared_task(name="game.deal")
# def game_deal ():