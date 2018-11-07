from random import randint
from easyAI import AI_Player, Negamax, SSS, DUAL, TT
import time


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


def play_game_time(game):
    start_time = time.time()
    game.play(verbose = False)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


def create_dual(depth):
    ai_algo_dual = DUAL(depth)
    return create_benchmark_game(ai_algo_dual)


def create_negamax(depth):
    ai_algo_neg = Negamax(depth)
    return create_benchmark_game(ai_algo_neg)


def create_sss(depth):
    ai_algo_sss = SSS(depth)
    return create_benchmark_game(ai_algo_sss)

def create_dual_tt(depth):
    ai_algo_dual = DUAL(depth,tt = TT())
    return create_benchmark_game(ai_algo_dual)


def create_negamax_tt(depth):
    ai_algo_neg = Negamax(depth,tt = TT())
    return create_benchmark_game(ai_algo_neg)


def create_sss_tt(depth):
    ai_algo_sss = SSS(depth,tt = TT())
    return create_benchmark_game(ai_algo_sss)


from games.Gomoku import Gomoku
#from games.Gomoku_optimized import Gomoku_optimized
from games.Gomoku_Strategic import Gomoku_Strategic

def create_benchmark_game(ai_algo):
    game = Gomoku([Benchmark_Player(), AI_Player(ai_algo)], 6)
    #game = Gomoku_optimized([Benchmark_Player(), AI_Player(ai_algo)], 6)
    #game = Gomoku_Strategic([Benchmark_Player(), AI_Player(ai_algo)], 6)
    return game


def test():
    f = open('result_original.csv', 'w')
    f.write("depth, Negamax, SSS, DUAL\n")
    nr_repetitions = 10
    nr_algorithms = 3
    max_depth = 6

    for d in range(1, max_depth+1):
        print "depth: ",d
        for algo in range(nr_algorithms):
            print "    algo: ",algo
            f.write(b'%d' % d)

            game = "No game yet"


            execution_time = 0.0

            for reps in range(nr_repetitions):
                # must create new instance of the game every time else the game cannot be restarted
                if algo == 0:
                    game = create_negamax_tt(d)
                elif algo == 1:
                    game = create_sss_tt(d)
                elif algo == 2:
                    game = create_dual_tt(d)

                execution_time += play_game_time(game)
            f.write(b', %f' % (execution_time / nr_repetitions))
        f.write('\n')
        print "\n"

    f.close()


if __name__ == "__main__":
    test()
