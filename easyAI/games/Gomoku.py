from easyAI import TwoPlayersGame
from easyAI.Player import Human_Player


class Gomoku(TwoPlayersGame):
    """ The board positions are numbered as follows:
            0 1 2
            3 4 5
            6 7 8
    """

    def __init__(self, players, size):
        self.players = players
        self.size = size
        self.board = [0 for i in range(self.size*self.size)]
        self.nplayer = 1  # player 1 starts.
        self.last_move = -1

    def possible_moves(self):
        return [i for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        self.board[int(move)] = self.nplayer
        self.last_move = int(move)

    def unmake_move(self, move):  # optional method (speeds up the AI)
        self.board[int(move)] = 0

    def lose(self):
        """ Has the opponent "five in line ?" """
        return self.find_five(self.board, self.nopponent)

    def is_over(self):
        return (self.possible_moves() == []) or self.lose()

    def show(self):
        print ('\n' + '\n'.join([
            ' '.join([['.', 'O', 'X'][self.board[3 * j + i]]
                      for i in range(3)])
            for j in range(3)]))

    def scoring(self):
        return -100 if self.lose() else 0

    def find_five(self, board, nplayer):
        """
        Returns True iff the player 'nplayer' has connected 5 (or more) pieces
        """
        length = 5
        y = self.last_move // self.size
        x = self.last_move % self.size

        #dir1
        curr_x = x
        curr_y = y
        found = 1
        for i in range(1,length - 1, 1):
            curr_x += i
            if curr_x < self.size:
                if board[curr_y * self.size + curr_x] == nplayer:
                    found +=1
        if found == length:
            return True


if __name__ == "__main__":
    from easyAI import AI_Player, Negamax

    ai_algo = Negamax(6)
    Gomoku([Human_Player(), AI_Player(ai_algo)]).play()