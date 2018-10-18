from random import randint
from games.ConnectFour import ConnectFour
from easyAI import AI_Player, Negamax, SSS, DUAL, TwoPlayersGame
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

    def __init__(self, name = 'Benchmark'):
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


def play_game_time(game):
    start_time = time.time()
    game.play()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


def create_dual(depth):
    ai_algo_dual = DUAL(depth)
    game = create_benchmark_game(ai_algo_dual)
    return game


def create_negamax(depth):
    ai_algo_neg = Negamax(depth)
    game = create_benchmark_game(ai_algo_neg)
    return game


def create_sss(depth):
    ai_algo_sss = SSS(depth)
    game = create_benchmark_game(ai_algo_sss)
    return game


def create_benchmark_game(ai_algo):
    game = ConnectFourOriginal([Benchmark_Player(), AI_Player(ai_algo)])
    return game


def test():
    file = open('result_original.csv', 'w')
    file.write("depth, Negamax, SSS, DUAL\n")
    nr_repetitions = 10
    nr_algorithms = 3
    max_depth = 3

    for d in range(1, max_depth+1):
        for algo in range(nr_algorithms):
            file.write(b'%d' % d)

            game = "No game yet"
            if algo == 0:
                game = create_negamax(d)
            elif algo == 1:
                game = create_sss(d)
            elif algo == 2:
                game = create_dual(d)

            execution_time = 0.0

            for reps in range(nr_repetitions):
                execution_time += play_game_time(game)
            file.write(b', %f' % (execution_time / nr_repetitions))
        file.write('\n')

    file.close()


if __name__ == "__main__":
    test()
