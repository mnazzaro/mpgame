'''
Description: This file handles the logic of the poker table. It is initialized
with a list of Player objects. The Player at index 0 in self.players is the 
button, and the player at index 1 is small blind. The list is rotated when a new 
round begins.

Author: Mark Nazzaro
'''

from typing import *
from player import Player
from random import randint

class Table:

    def __init__(self, players: List[Player]):
        self.players = players
        
    def add_player(self, player: Player):
        self.players.insert(randint(0, len(self.players) - 1), player)
    
    def remove_player(self, player: Player):
        self.players.remove(player)

    def shift_button(self):
        temp = self.players[1:]
        temp.append(self.players[0])
        self.players = temp


# if __name__ == '__main__':
#     table = Table([Player(0, None), Player(1, None), Player(2, None)])
#     print (table.players)
#     table.shift_button()
#     print (table.players)