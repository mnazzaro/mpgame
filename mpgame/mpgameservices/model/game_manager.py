from typing import Dict, List

from json import dump, load

import pokerface

from .player import Player
from .hand import Hand

# Need to figure out event system

# def __init__ (self, game_config):
#     # Future will have a config to determine game type, etc.
#     self.status = 0 # Game no players, just started
#     self.players = []
#     self.current_hand = None # Hand(players, 0.5, 1, 0)
#     self.game_config = game_config
#     self.act_state = []

def add_player (self, player: Player) -> Dict:
    self.players.append(player) # This will likely need to be adjusted- maybe check for None's in the list and replace the first
    if len(self.players) >= 2:
        # TODO:
        # Generate public data json for broadcast
        # broadcast
        pass

def serialize_hand (hand: Hand) -> List[str]:
    obj = {}
    obj['hand_state'] = hand.get_actions()
    return dump(obj)

def deserialize_hand (hand_state: Dict, game_config: Dict):
    return Hand(game_config['betting_order'], game_config['sb'], 
                game_config['bb'], game_config['ante'], hand_state['hand_state'])
    
        
