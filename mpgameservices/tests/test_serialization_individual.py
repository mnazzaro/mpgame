import sys
sys.path.append('..')

from ..model.hand import Hand
from ..model.player import Player

from unittest import TestCase

class TestAuthenticationController (TestCase):
        
    def setUp (self):
        p1 = Player(0, 200)
        p2 = Player(0, 200)
        p3 = Player(0, 200)
        self.hand = Hand([p1, p2, p3], 1, 2, 0, [])

    def test_deal_flop (self):
        hands = []
        for hand in self.hand.deal_all_hole():
            hands.append(hand)
        self.hand.check_call()
        self.hand.check_call()
        self.hand.check_call()
        self.hand.deal_board()
        print(self.hand.get_actions())
        self.assertEqual(self.hand.get_actions()[-1].split()[0], 'db') 

    def test_deal_turn (self):
        hands = []
        for hand in self.hand.deal_all_hole():
            hands.append(hand)
        self.hand.check_call()
        self.hand.check_call()
        self.hand.check_call()
        self.hand.deal_board()
        self.hand.check_call()
        self.hand.check_call()
        self.hand.check_call()
        self.hand.deal_board()
        print(self.hand.get_actions())
        self.assertEqual(self.hand.get_actions()[-1].split()[0], 'db') 


