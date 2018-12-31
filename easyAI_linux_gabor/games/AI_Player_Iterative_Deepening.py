from Negamax_Iterative_Deepening import Negamax_Iterative_Deepening
from copy import deepcopy
import time
from easyAI import TT
try:
    from colorama import init
    init()
    from colorama import Fore, Back, Style
except ImportError:
    print("Sorry, this example requires Colorama installed !")
    raise

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
        max_alpha = 0
        for depth in range(1, 20):
            ai = Negamax_Iterative_Deepening(depth=depth, tt=self.tt)
            move, alpha = ai(game_copy, timeout=self.max_time)
            if depth == 1 and alpha == 100:  # can win with first move
                return move
            if time.time() < self.max_time:
                max_alpha = max(max_alpha, abs(alpha))
                last = move
                print Fore.BLUE + ("depth:%d move %s alpha %s max_alpha %d" % (depth, move, alpha, max_alpha)) + Style.RESET_ALL
            else:
                if abs(alpha) > max_alpha:#even if depth was unfinished, the move is good
                    last = move
                    max_alpha = abs(alpha)
                print Fore.RED + ("depth:%d move %s alpha %s max_alpha %d" % (depth, move, alpha, max_alpha)) + Style.RESET_ALL
                break
        return last
