from games.Gomoku_Strategic import Gomoku_Strategic
from games.AI_Player_Iterative_Deepening import AI_Player_Iterative_Deepening
try:
    import numpy as np
except ImportError:
    print("Sorry, this example requires Numpy installed !")
    raise
from easyAI import Human_Player

def test1():
    board = np.array([[0, 0, 0, 0, 0, 0],
                      [0, 2, 0, 0, 0, 0],
                      [0, 2, 0, 0, 0, 0],
                      [0, 2, 0, 0, 0, 0],
                      [0, 0, 2, 2, 2, 0],
                      [0, 0, 0, 0, 0, 0]])

    return board


def run_test(timeout):
    board = test1()
    game = Gomoku_Strategic([AI_Player_Iterative_Deepening(timeout=timeout), Human_Player()], 6, board)
    game.play()
    if game.lose():
        print("Player %d wins!" % game.nopponent)
    else:
        print("Draw!")


if __name__ == "__main__":
    timeout = 15#5 seconds
    run_test(timeout)