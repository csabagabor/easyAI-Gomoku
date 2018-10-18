from random import randint
from games.ConnectFour import ConnectFour
from easyAI import Human_Player, AI_Player, Negamax, SSS, DUAL,TwoPlayersGame
import time

try:
    import numpy as np
except ImportError:
    print("Sorry, this example requires Numpy installed !")
    raise

class Benchmark_Player:
    """
    Class for a benchmark player, which moves immediately by random
    """

    def __init__(self, name = 'Human'):
        self.name = name

    def ask_move(self, game):
        possible_moves = game.possible_moves()
        move = possible_moves[randint(0, len(possible_moves)-1)]
        return move

class ConnectFourOriginal(TwoPlayersGame):
    """
    The game of Connect Four, as described here:
    http://en.wikipedia.org/wiki/Connect_Four
    """

    def __init__(self, players, board = None):
        self.players = players
        self.board = board if (board != None) else (
            np.array([[0 for i in range(7)] for j in range(6)]))
        self.nplayer = 1 # player 1 starts.

        self.POS_DIR = np.array([[[i, 0], [0, 1]] for i in range(6)] +
                                [[[0, i], [1, 0]] for i in range(7)] +
                                [[[i, 0], [1, 1]] for i in range(1, 3)] +
                                [[[0, i], [1, 1]] for i in range(4)] +
                                [[[i, 6], [1, -1]] for i in range(1, 3)] +
                                [[[0, i], [1, -1]] for i in range(3, 7)])

    def possible_moves(self):
        return [i for i in range(7) if (self.board[:, i].min() == 0)]

    def make_move(self, column):
        line = np.argmin(self.board[:, column] != 0)
        self.board[line, column] = self.nplayer

    def show(self):
        pass

    def lose(self):
        return self.find_four(self.board, self.nopponent)

    def is_over(self):
        return (self.board.min() > 0) or self.lose()

    def scoring(self):
        return -100 if self.lose() else 0


    def find_four(self, board, nplayer):
        """
        Returns True iff the player has connected  4 (or more)
        This is much faster if written in C or Cython
        """
        for pos, direction in self.POS_DIR:
            streak = 0
            while (0 <= pos[0] <= 5) and (0 <= pos[1] <= 6):
                if board[pos[0], pos[1]] == nplayer:
                    streak += 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
                pos = pos + direction
        return False


def run_negamax(depth):
    ai_algo_neg = Negamax(depth)
    game = ConnectFourOriginal([Benchmark_Player(), AI_Player(ai_algo_neg)])
    game.play()

def test():
    file = open('result_original.csv', 'w')
    file.write("Negamax, SSS")
    nr_repetitions = 10
    nr_algorithms = 5
    for algo in range(1,nr_algorithms,1):
        for d in range(1, 7, 1):
            execution_time = 0.0
            for reps in range(1, nr_repetitions, 1):

                start_time = time.time()
                if algo == 1:
                    execution_time +=run_negamax()
                    if algo == nr_repetitions
                elif algo == 2:
                    pass
                end_time = time.time()
                execution_time += end_time - start_time


    file.close()

if __name__ == "__main__":
    test()
