from games.Negamax_Iterative_Deepening import Negamax_Iterative_Deepening
from copy import deepcopy
import time
from easyAI import TT


class AI_Player_Iterative_Deepening:
    """
    Class for an AI player. This class must be initialized with an
    AI algortihm, like ``AI_Player( Negamax(9) )``
    """

    def __init__(self, timeout=5, name='AI_iterative'):
        self.name = name
        self.move = {}
        self.tt = TT()
        self.timeout = timeout

    def ask_move(self, game):
        self.max_time = time.time() + self.timeout
        last = game.possible_moves()[0]
        game_copy = deepcopy(game)
        for depth in range(1, 4):
            ai = Negamax_Iterative_Deepening(depth=depth, tt=self.tt)
            move, alpha = ai(game_copy, timeout=self.max_time)
            print move, alpha
            if depth == 1 and alpha == 100:#can win with first move
                return move
            # if depth == 2 and alpha < -99:#certain lose if not immediate counter-attack
            #     return move
            if move != 9999:
                last = move
            else:
                break
            print("depth:%d" % depth)
        return last