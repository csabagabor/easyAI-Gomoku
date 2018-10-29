import numpy as np
cimport numpy as np

cpdef int find_five(nplayer,np.ndarray[long, ndim=2] board,size, last_move_x,last_move_y):
    """
    Returns True iff the player 'nplayer' has connected 5 (or more) pieces
    """
    length = 5
    x = last_move_x
    y = last_move_y


    if x != -1 and y != -1:

        if horizontal_win(board,size,x, y, length, nplayer):
            return 1
        if vertical_win(board,size,x, y, length, nplayer):
            return 1
        if diagonal_right_up_win(board,size,x, y, length, nplayer):
            return 1
        if diagonal_left_down_win(board,size,x, y, length, nplayer):
            return 1

        return 0

    return 0

def horizontal_win(board,size, x, y, length, nplayer):
    # horizontal direction
    curr_x = x
    curr_y = y
    left = 0  # how many dots on the left
    right = 0  # and on the right respectively

    # search for dots at right
    for i in range(1, length):
        curr_x = x + i
        if curr_x < size:
            if board[curr_y, curr_x] == nplayer:
                right += 1
            else:
                break
    # search for dots at left
    for i in range(1, length):
        curr_x = x - i
        if curr_x >= 0:
            if board[curr_y, curr_x] == nplayer:
                left += 1
            else:
                break

    if right + left + 1 == length:
        return True
    return False

def vertical_win(board,size,x, y, length, nplayer):
    # vertical direction
    curr_x = x
    curr_y = y
    top = 0  # how many dots on the top direction
    down = 0  # and on the bottom direction

    # search for dots on top
    for i in range(1, length):
        curr_y = y - i
        if curr_y >= 0:
            if board[curr_y, curr_x] == nplayer:
                top += 1
            else:
                break

    # search for dots on bottom
    for i in range(1, length):
        curr_y = y + i
        if curr_y < size:
            if board[curr_y, curr_x] == nplayer:
                down += 1
            else:
                break

    if top + down + 1 == length:
        return True
    return False


def diagonal_right_up_win(board,size,x, y, length, nplayer):
    # diagonal direction
    curr_x = x
    curr_y = y
    top = 0  # how many dots on the top direction
    down = 0  # and on the bottom direction

    # search for dots on top
    for i in range(1, length):
        curr_y = y - i
        curr_x = x + i
        if curr_y >= 0 and curr_x < size:
            if board[curr_y, curr_x] == nplayer:
                top += 1
            else:
                break

    # search for dots on bottom
    for i in range(1, length):
        curr_y = y + i
        curr_x = x - i
        if curr_y < size and curr_x >= 0:
            if board[curr_y, curr_x] == nplayer:
                down += 1
            else:
                break

    if top + down + 1 == length:
        return True
    return False

def diagonal_left_down_win(board,size, x, y, length, nplayer):
    # diagonal direction
    curr_x = x
    curr_y = y
    top = 0  # how many dots on the top direction
    down = 0  # and on the bottom direction

    # search for dots on top
    for i in range(1, length):
        curr_y = y + i
        curr_x = x + i
        if curr_y < size and curr_x < size:
            if board[curr_y, curr_x] == nplayer:
                down += 1
            else:
                break

    # search for dots on bottom
    for i in range(1, length):
        curr_y = y - i
        curr_x = x - i
        if curr_y >= 0 and curr_x >= 0:
            if board[curr_y, curr_x] == nplayer:
                top += 1
            else:
                break

    if top + down + 1 == length:
        return True
    return False