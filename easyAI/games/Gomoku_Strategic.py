from easyAI import TwoPlayersGame, id_solve, df_solve
from easyAI.Player import Human_Player
from collections import OrderedDict
from games.AI_Player_Iterative_Deepening import AI_Player_Iterative_Deepening

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

class Gomoku_Strategic(TwoPlayersGame):
    """ The board positions are numbered as follows:
            0 1 2
            3 4 5
            6 7 8
    """

    def __init__(self, players, size=9, init_board = None):
        if size >= 10:
            raise ValueError('size should be less than 10')
        self.players = players
        self.haslost = None
        self.size = size
        self.board = np.array([[0 for i in range(self.size)] for j in range(self.size)])
        self.nplayer = 1  # player 1 starts.
        self.last_move_x = -1
        self.last_move_y = -1
        #improve AI (works for 1 AI only)
        self.ai_player = -1
        if isinstance(players[0], AI_Player_Iterative_Deepening):
            self.ai_player = 1
        elif isinstance(players[1],AI_Player_Iterative_Deepening):
            self.ai_player = 2
        elif isinstance(players[0], AI_Player):
            self.ai_player = 1
        elif isinstance(players[1], AI_Player):
            self.ai_player = 2
        if init_board is not None:
            self.board = init_board


    def possible_moves(self):
        possible_moves = []
        if self.ai_player == self.nplayer:#AI player moves - reduce set of possible moves for a faster AI
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i, j] == 0:  # AI can move only to empty positions
                        if j + 1 < self.size and self.board[i][j + 1] != 0:  # AI can move only to positions which have non-empty neighbours - faster AI
                            possible_moves.append(self.coords_to_move(j, i))
                            continue
                        if j - 1 >= 0 and self.board[i][j - 1] != 0:
                            possible_moves.append(self.coords_to_move(j, i))
                            continue
                        if i + 1 < self.size:
                            if self.board[i + 1][j] != 0:
                                possible_moves.append(self.coords_to_move(j, i))
                                continue
                            if j + 1 < self.size and self.board[i + 1][j + 1] != 0:
                                possible_moves.append(self.coords_to_move(j, i))
                                continue
                            if j - 1 >= 0 and self.board[i + 1][j - 1] != 0:
                                possible_moves.append(self.coords_to_move(j, i))
                                continue
                        if i - 1 >= 0:
                            if self.board[i - 1][j] != 0:
                                possible_moves.append(self.coords_to_move(j, i))
                                continue
                            if j + 1 < self.size and self.board[i - 1][j + 1] != 0:
                                possible_moves.append(self.coords_to_move(j, i))
                                continue
                            if j - 1 >= 0 and self.board[i - 1][j - 1] != 0:
                                possible_moves.append(self.coords_to_move(j, i))
                                continue
        if possible_moves == []: # first move for AI OR other player
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

    def get_coords_from_move(self, move):
        row = int(move[0])
        column = ord(move[1]) - ord('a')  # letter
        return [row, column]

    def coords_to_move(self,x,y):
        return str(y) + chr(x + ord('a'))

    def unmake_move(self, move):  # optional method (speeds up the AI)
        coords = self.get_coords_from_move(move)
        row = coords[0]
        column = coords[1]
        self.board[row, column] = 0
        self.last_move_x = -1 #last move doesn't need to be saved because the player cannot "win" by unmaking his move
        self.last_move_y = -1

    def lose(self):
        self.haslost = self.find_five(self.nopponent)
        return self.haslost

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
        if self.haslost != None: #make AI faster, checks connected line only once in a single step
            if self.haslost:
                self.haslost = None
                return -100
            else:
                self.haslost = None
        elif self.lose():
                return -100
        strategic_score = self.strategic_score(self.board, self.size, self.nplayer)
        if strategic_score > 100000:
            return 100
        strategic_score -= 1.2*self.strategic_score(self.board, self.size, self.nopponent)
        if strategic_score < -100000:
            return -100
        if strategic_score > 0:
            return 0
        if strategic_score < -90:
            return -90
        return strategic_score

    def win(self, board, size, nplayer):
        five = str(nplayer) * 5
        for i in range(0, size):
            row = ''.join([str(item) for item in board[i, :]])
            if five in row:
                return True
        for j in range(0, size):
            column = ''.join([str(item) for item in board[:, j]])
            if five in column:
                return True
        for k in range(-size + 1, size - 1):  # diagonal
            diagonal = ''.join([str(item) for item in board.diagonal(k)])
            if five in diagonal:
                return True
            diagonal = ''.join([str(item) for item in board[::-1].diagonal(k)])
            if five in diagonal:
                return True
        return False

    def strategic_score(self, board, size, nplayer):
        threats = OrderedDict() #key - name of threat; value - (representation, score)
        # !!!! order of items is important
        threats['five'] = (str(nplayer) * 5, 100000)  # certain loose/win
        threats['open_four'] = ("0"+str(nplayer)*4+"0", 90) #certain loose/win
        threats['open_three'] = ("0"+str(nplayer)*3+"0", 25)
        threats['closed_four'] = (str(nplayer)*4+"0", 30)
        threats['closed_four2'] = ("0" + str(nplayer) * 4, 30)
        threats['closed_three'] = (str(nplayer) * 3 + "00", 15) #we must have 2 zeros cause cannot connect 5 if there are 4 spots
        threats['closed_three2'] = ("00" + str(nplayer) * 3, 15)
        score = 0

        for i in range(0, size):
            row = ''.join([str(item) for item in board[i, :]])
            score += self.threats_in_line(threats, row, nplayer)
        for j in range(0, size):
            column = ''.join([str(item) for item in board[:, j]])
            score += self.threats_in_line(threats, column, nplayer)
        for k in range(-size + 1, size - 1): #diagonal
            diagonal = ''.join([str(item) for item in board.diagonal(k)])
            if len(diagonal) >= 5: #cannot create threat in smaller area
                score += self.threats_in_line(threats, diagonal, nplayer)
            diagonal = ''.join([str(item) for item in board[::-1].diagonal(k)])
            if len(diagonal) >= 5:
                score += self.threats_in_line(threats, diagonal, nplayer)
        return score

    def threats_in_line(self, threats, row, nplayer):
        threat_left = True
        score = 0
        while threat_left and row.count(str(nplayer)) > 2:
            threat_left = False
            for name, v in threats.items():
                if v[0] in row:
                    threat_left = True
                    score += v[1]

                    row = row.replace(v[0], '5' * len(v[0]))  # caution - this works with simple
                    # threats but not with complicated ones
                    # if 2 different threats want to use the same free space,
                    # only one can use it....
        return score

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
        elif self.win(self.board, self.size, self.nplayer):
            return True
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
    r, d, m = id_solve(Gomoku_Strategic, range(2, 7), win_score=100, tt=tt)
    print r,d,m


def solve_game_df():
    ai_algo = Negamax(10, tt=TT())
    game = Gomoku_Strategic([Human_Player(), AI_Player(ai_algo)], 5)
    result = df_solve(game, win_score=100, maxdepth=10, tt=TT(), depth=0)
    print result


def play_game_simple(size = 6):
    ai_algo = Negamax(4)
    game = Gomoku_Strategic([Human_Player(), AI_Player(ai_algo)], size)
    game.play()
    if game.lose():
        print("Player %d wins!" % game.nopponent)
    else:
        print("Draw!")


def play_game_transposition_table(size = 6):
    ai_algo = Negamax(4, tt = TT())
    game = Gomoku_Strategic([Human_Player(), AI_Player(ai_algo)], size)
    game.play()
    if game.lose():
        print("Player %d wins!" % game.nopponent)
    else:
        print("Draw!")


def play_iterative_deepening(size = 6, timeout = 5):
    game = Gomoku_Strategic([Human_Player(), AI_Player_Iterative_Deepening(timeout=timeout)], size)
    game.play()
    if game.lose():
        print("Player %d wins!" % game.nopponent)
    else:
        print("Draw!")


if __name__ == "__main__":
    from easyAI import AI_Player, Negamax, SSS, DUAL, TT

    #play_game_simple(size = 6)
    #play_game_transposition_table(size = 6)
    play_iterative_deepening(size=9, timeout=5)
    #solve_game()
    #solve_game_df()

