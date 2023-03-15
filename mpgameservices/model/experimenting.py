from pokerface import Stakes, NoLimitTexasHoldEm, PokerPlayer, Card, PokerNature

actions = []
player_index = 0
game = NoLimitTexasHoldEm(Stakes(0, (1, 2)), [200, 200, 200])

while game.nature.can_deal_hole():
    game.nature.deal_hole()
    holes = game.players[player_index].hole
    actions.append(f'dh {str(holes[0].__repr__())}{str(holes[1].__repr__())}')
    player_index += 1
    print (holes)

game2 = NoLimitTexasHoldEm(Stakes(0, (1, 2)), [200, 200, 200])
game2.act(*actions)
print (game2.players[0].hole)