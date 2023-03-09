from celery import shared_task 
from celery.signals import worker_process_init, worker_process_shutdown

import sys
sys.path.append('..')
from mpgameservices.model.game_manager import deserialize_hand

import functools
from typing import Callable 


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

