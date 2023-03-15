from celery import shared_task 
from celery.signals import worker_process_init, worker_process_shutdown

import sys
sys.path.append('..')
from mpgameservices.model.game_manager import deserialize_hand
from mpgameservices.model import hand, player

import redis
import json

import functools
from typing import Callable, Dict

redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

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

@shared_task(name="tasks.add_together")
def add_together (x, y):
    return x + y

@shared_task(name="game.add_player")
def add_player (player: Dict):
    if redis.exists('players'):
        players = json.loads(redis.get('players'))
        players['players'].append(player)
        redis.set('players', json.dumps(players))
    else:
        redis.set('players', json.dumps({'players' : [player]}))
    return json.loads(redis.get('players'))

# @shared_task(name="game.deal")
# def game_deal ()