#  Optimizing the Gomoku game with easyAI

>Note
This project is based on easyAI: https://github.com/Zulko/easyAI

# Installing the tool 
1. Make sure Python is installed on the computer(check it with `python --version`). If it is not, install it from the oﬃcial Python website(. This tool works best with Python 2.7 but it works with Python 3 as well.
2. Make sure pip is installed on the computer. Pip comes pre-installed with new Python releases.
3. Dowload the source code from Github unzip it and then `sudo python setup.py install`
4. Some examples need Numpy to be installed, so just type `sudo pip install Nump`y
5. If you need Flask to run the TicTacToe-Flask example: `sudo pip install Flask`
6. If you need Kivy to run the Knights-Kivy example: `sudo pip install Kivy`

# About
This project tries contains an AI for the well-known game Gomoku(https://en.wikipedia.org/wiki/Gomoku). It tries to combine several concepts and algorithms to come up with a really competitive algorithm. These things are:
- **Negamax with timeout**: Negamax with timeout means that the class receives a variable indicating a duration and it can calculate moves only if the duration is not over. After time is over it has to return the best move it has seen so far. This is useful in this game because the AI can reach a depth of 5 in a reasonable amount of time sometimes but other times it can reach only a depth of 3 in the same amount of time.
- **Iterative deepening**: With iterative deepening if the algorithm ﬁnds a very good/very bad move it will further evaluate that branch deeper to see if there is an even better/worse outcome. This approach works for Gomoku because some moves can be rejected from the beginning because they won’t have good outcome. In this way a low depth can be maintained for the AI search tree while some branches will have higher depths resulting in a faster execution time.
- **Heuristic function**
The AI is a defensive AI meaning that the same board position for the opponent means a higher score than the same position for the current player. Some positions which are examined are: open four, closed four, open three, closed three.
- **Cython**
- **SSS* **


