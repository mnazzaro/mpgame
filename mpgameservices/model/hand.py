from typing import List, Generator, Tuple, Optional
from pokerface import Stakes, NoLimitTexasHoldEm, PokerPlayer, Card, PokerNature
from .player import Player

class Hand:

    def __init__ (self, betting_order: List[Player], sb: float, bb: float, ante: float, actions: Optional[List[str]] = None):
        # Just assume NL Texas Holdem for now
        self._game = NoLimitTexasHoldEm(Stakes(ante, (sb, bb)), Hand._get_stacks(betting_order))
        self._index_player_map = dict(zip(list(range(len(betting_order))), betting_order))
        if actions is not None:
            self._actions_string = actions
            self._game.act(*actions)
        else:
            self._actions_string = []

    # STATIC METHODS
    def _get_stacks (players: List[Player]) -> List[float]:
        return tuple(map(lambda player: player.stack, players))

    # CLASS METHODS
    def _player_from_index (self, index):
        return self._index_player_map.get(index)
    
    @property
    def check_call_amount (self) -> float:
        return self.current_actor().check_call_amount
    
    def raise_min_amount (self) -> float:
        return self.current_actor().bet_raise_min_amount
    
    def valid_bet (self, amount: float) -> bool:
        return amount == self.check_call_amount() \
            or (amount >= self.raise_min_amount()
                and amount <= self.current_actor().effective_stack)
    
    def pot (self) -> int:
        return self._game.pot
    
    def side_pots (self) -> List[int]:
        return list(self._game.side_pots)
    
    def current_actor (self) -> PokerPlayer | PokerNature:
        return self._game.actor
    
    def hand_over (self) -> bool:
        return self._game.is_terminal()
    
    def deal_all_hole (self) -> Generator[Tuple[Card, Card], None, None]:
        player_index = 0
        while self._game.nature.can_deal_hole():
            self._game.nature.deal_hole()
            holes = self._game.players[player_index].hole
            self._actions_string.append(f'dh {holes[0].__repr__()}{holes[1].__repr__()}') 
            player_index += 1
            yield holes

    def deal_board (self) -> List[Card]:
        board_length_before = len(self._game.board)
        self._game.nature.deal_board()
        board_length = len(self._game.board)
        new_additions = ''.join(
            list(
                map(
                    lambda card: str(card),
                    self._game.board[board_length_before - board_length:]
                    )
                )
            )
            
        self._actions_string.append(f'db {new_additions}' )
        return self._game.board
    
    def fold (self):
        self.current_actor().fold()
        self._actions_string.append('f')

    def bet (self, amount: float):
        player = self.current_actor()

        if amount == self.check_call_amount():
            player.check_call()
            self._actions_string.append('cc')
        else:
            player.bet_raise(amount)
            self._actions_string.append(f'br {amount}')

    def check_call (self):
        self.current_actor().check_call()
        self._actions_string.append('cc')

    def get_actions (self) -> List[str]:
        return self._actions_string

