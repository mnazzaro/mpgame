from typing import List, Generator, Tuple, Dict
from pokerface import Stakes, NoLimitTexasHoldEm, PokerPlayer, Card, PokerNature
from .player import Player

class Hand:

    def __init__ (self, betting_order: List[Player], sb: float, bb: float, ante: float, actions: Dict):
        # Just assume NL Texas Holdem for now
        self._game = NoLimitTexasHoldEm(Stakes(ante, (sb, bb)), Hand._get_stacks(betting_order))
        self._index_player_map = dict(zip(list(range(len(betting_order))), betting_order))
        self._game.act(actions)

    # STATIC METHODS
    def _get_stacks (players: List[Player]) -> List[float]:
        return tuple(map(lambda player: player.stack))

    # CLASS METHODS
    def _player_from_index (self, index):
        return self._index_player_map.get(index)
    
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
            yield self._game.players[0].hole

    def deal_board (self) -> List[Card]:
        self._game.nature.deal_board()
        return self._game.board
    
    def fold (self):
        self.current_actor().fold()

    def bet (self, amount: float):
        player = self.current_actor()

        if amount == self.check_call_amount():
            player.check_call()
        else:
            player.bet_raise(amount)

    

