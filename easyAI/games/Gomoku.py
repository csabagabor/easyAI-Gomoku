from easyAI import TwoPlayersGame, id_solve, df_solve
from easyAI.Player import Human_Player


try:
    from colorama import init
    init()
    from colorama import Fore, Back, Style
except ImportError:
    print("Sorry, this example requires Colorama installed !")
    raise

try:
    import numpy as np
except ImportError:
    print("Sorry, this example requires Numpy installed !")
    raise


class Gomoku(TwoPlayersGame):
    """ The board positions are numbered as follows:
            0 1 2
            3 4 5
            6 7 8
    """

    def __init__(self, players, size=9):
        if size >= 10:
            raise ValueError('size should be less than 10')
        self.players = players
        self.size = size
        self.board = np.array([[0 for i in range(self.size)] for j in range(self.size)])
        self.nplayer = 1  # player 1 starts.
        self.last_moves_array = []
        self.last_move_x = -1
        self.last_move_y = -1

    def possible_moves(self):
        possible_moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == 0:
                    possible_moves.append(str(i) + chr(j + ord('a')))
        return possible_moves

    def make_move(self, move):
        coords = self.get_coords_from_move(move)
        row = coords[0]
        column = coords[1]
        self.board[row, column] = self.nplayer
        self.last_move_x = column
        self.last_move_y = row
        self.last_moves_array.append([column, row])

    def get_coords_from_move(self, move):
        row = int(move[0])
        column = ord(move[1]) - ord('a')  # letter
        return [row, column]


    def lose(self):
        """ Has the opponent "five in line ?" """
        return self.find_five(self.nopponent)

    def is_over(self):
        return (self.possible_moves() == []) or self.lose()

    def ttentry(self):
        return "".join([".0X"[i] for i in self.board.flatten()])

    def show(self):
        board_str = "  "
        for i in range(self.size):
            board_str += chr(i + ord('a'))
        board_str += "\n  "
        for i in range(self.size):
            board_str += "#"
        board_str += "\n"
        for i in range(self.size):
            board_str += str(i) + "#"
            for j in range(self.size):
                if self.board[i, j] == 1:
                    board_str += Fore.GREEN + "1" + Style.RESET_ALL
                elif self.board[i, j] == 2:
                    board_str += Fore.RED + "2" + Style.RESET_ALL
                else:
                    board_str += str(self.board[i, j])
            board_str += "\n"
        print board_str

    def scoring(self):
        return -100 if self.lose() else 0

    def find_five(self, nplayer):
        """
        Returns True iff the player 'nplayer' has connected 5 (or more) pieces
        """
        length = 5
        x = self.last_move_x
        y = self.last_move_y


        if x != -1 and y != -1:

            if self.horizontal_win(x, y, length, nplayer):
                return True
            if self.vertical_win(x, y, length, nplayer):
                return True
            if self.diagonal_right_up_win(x, y, length, nplayer):
                return True
            if self.diagonal_left_down_win(x, y, length, nplayer):
                return True

            return False

        return False

    def horizontal_win(self,x, y, length, nplayer):
        # horizontal direction
        curr_x = x
        curr_y = y
        left = 0  # how many dots on the left
        right = 0  # and on the right respectively

        # search for dots at right
        for i in range(1, length):
            curr_x = x + i
            if curr_x < self.size:
                if self.board[curr_y, curr_x] == nplayer:
                    right += 1
                else:
                    break
        # search for dots at left
        for i in range(1, length):
            curr_x = x - i
            if curr_x >= 0:
                if self.board[curr_y, curr_x] == nplayer:
                    left += 1
                else:
                    break

        if right + left + 1 == length:
            return True
        return False

    def vertical_win(self,x, y, length, nplayer):
        # vertical direction
        curr_x = x
        curr_y = y
        top = 0  # how many dots on the top direction
        down = 0  # and on the bottom direction

        # search for dots on top
        for i in range(1, length):
            curr_y = y - i
            if curr_y >= 0:
                if self.board[curr_y, curr_x] == nplayer:
                    top += 1
                else:
                    break

        # search for dots on bottom
        for i in range(1, length):
            curr_y = y + i
            if curr_y < self.size:
                if self.board[curr_y, curr_x] == nplayer:
                    down += 1
                else:
                    break

        if top + down + 1 == length:
            return True
        return False


    def diagonal_right_up_win(self,x, y, length, nplayer):
        # diagonal direction
        curr_x = x
        curr_y = y
        top = 0  # how many dots on the top direction
        down = 0  # and on the bottom direction

        # search for dots on top
        for i in range(1, length):
            curr_y = y - i
            curr_x = x + i
            if curr_y >= 0 and curr_x < self.size:
                if self.board[curr_y, curr_x] == nplayer:
                    top += 1
                else:
                    break

        # search for dots on bottom
        for i in range(1, length):
            curr_y = y + i
            curr_x = x - i
            if curr_y < self.size and curr_x >= 0:
                if self.board[curr_y, curr_x] == nplayer:
                    down += 1
                else:
                    break

        if top + down + 1 == length:
            return True
        return False

    def diagonal_left_down_win(self, x, y, length, nplayer):
        # diagonal direction
        curr_x = x
        curr_y = y
        top = 0  # how many dots on the top direction
        down = 0  # and on the bottom direction

        # search for dots on top
        for i in range(1, length):
            curr_y = y + i
            curr_x = x + i
            if curr_y < self.size and curr_x < self.size:
                if self.board[curr_y, curr_x] == nplayer:
                    down += 1
                else:
                    break

        # search for dots on bottom
        for i in range(1, length):
            curr_y = y - i
            curr_x = x - i
            if curr_y >= 0 and curr_x >= 0:
                if self.board[curr_y, curr_x] == nplayer:
                    top += 1
                else:
                    break

        if top + down + 1 == length:
            return True
        return False


def solve_game():
    tt = TT()
    r, d, m = id_solve(Gomoku, range(2, 20), win_score=100, tt=tt)
    print r,d,m


def solve_game_df():
    ai_algo = Negamax(10, tt=TT())
    game = Gomoku([Human_Player(), AI_Player(ai_algo)], 5)
    result = df_solve(game, win_score=100, maxdepth=10, tt=TT(), depth=0)
    print result


def play_game_simple():
    ai_algo = Negamax(5)
    game = Gomoku([Human_Player(), AI_Player(ai_algo)], 5)
    game.play()
    if game.lose():
        print("Player %d wins!" % game.nopponent)
    else:
        print("Draw!")


def play_game_transposition_table():
    ai_algo = Negamax(5, tt = TT())
    game = Gomoku([Human_Player(), AI_Player(ai_algo)], 5)
    game.play()
    if game.lose():
        print("Player %d wins!" % game.nopponent)
    else:
        print("Draw!")


if __name__ == "__main__":
    from easyAI import AI_Player, Negamax, SSS, DUAL, TT

    play_game_simple()
    #play_game_transposition_table()
    #solve_game()
    #solve_game_df()

