from games.Gomoku_Strategic import Gomoku_Strategic
from games.AI_Player_Iterative_Deepening import AI_Player_Iterative_Deepening
try:
    import numpy as np
except ImportError:
    print("Sorry, this example requires Numpy installed !")
    raise
from easyAI import Human_Player

def test(nr):
    board = {}
    board["1"] = np.array([[0, 0, 0, 0, 0, 0],
                          [0, 2, 0, 0, 0, 0],
                          [0, 2, 0, 0, 0, 0],
                          [0, 2, 0, 0, 0, 0],
                          [0, 0, 2, 2, 2, 0],
                          [0, 0, 0, 0, 0, 0]])

    board["2"] = np.array([[2, 2, 2, 2, 0, 0],
                           [1, 1, 2, 0, 0, 0],
                           [1, 1, 2, 0, 0, 0],
                           [1, 1, 1, 2, 0, 0],
                           [2, 0, 0, 0, 2, 0],
                           [1, 1, 0, 0, 0, 0]])

    board["3"] = np.array([[1, 1, 1, 1, 0, 0],
                           [2, 2, 1, 0, 0, 0],
                           [2, 2, 1, 0, 0, 0],
                           [2, 2, 2, 1, 0, 0],
                           [1, 0, 0, 0, 1, 0],
                           [2, 2, 0, 0, 0, 0]])

    board["4"] = np.array([[2, 0, 0, 0, 0, 0],
                           [0, 2, 1, 2, 0, 0],
                           [0, 0, 1, 0, 0, 0],
                           [2, 0, 1, 2, 0, 0],
                           [1, 2, 1, 1, 1, 0],
                           [2, 2, 2, 0, 0, 0]])

    board["5"] = np.array([[2, 0, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])

    board["6"] = np.array([[2, 0, 0, 0, 0, 0],
                           [0, 2, 0, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0],
                           [0, 0, 0, 2, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])

    board["7"] = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 2, 0, 0],
                           [0, 0, 2, 0, 0, 0],
                           [0, 2, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])

    board["8"] = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 2, 0],
                           [0, 2, 2, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0],
                           [0, 2, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])

    board["9"] = np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 2, 0],
                           [0, 2, 2, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0],
                           [0, 2, 0, 0, 0, 0],
                           [2, 0, 0, 0, 0, 0]])

    board["10"] = np.array([[0, 0, 0, 0, 0, 2],
                           [0, 0, 0, 0, 2, 0],
                           [0, 2, 2, 2, 0, 0],
                           [0, 0, 2, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])

    board["11"] = np.array([[1, 0, 0, 0, 0, 0],
                               [0, 1, 0, 0, 0, 0],
                               [0, 0, 1, 1, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 1, 0, 0]])

    board["12"] = np.array([[1, 1, 0, 1, 0, 0],
                               [0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0]])

    board["empty"] = np.array([[0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0]])

    return board[str(nr)]


def run_test(nr=1, timeout=5):
    board = test(nr)
    game = Gomoku_Strategic([AI_Player_Iterative_Deepening(timeout=timeout), Human_Player()], 6, board)
    game.play()
    if game.lose():
        print("Player %d wins!" % game.nopponent)
    else:
        print("Draw!")


if __name__ == "__main__":
    timeout = 5#5 seconds
    run_test(12, timeout)