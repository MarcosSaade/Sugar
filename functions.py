import math
from settings import *


def print_board(board):
    print(board[0], board[1], board[2])
    print('-------------------------' * 3)
    print(board[3], board[4], board[5])
    print('-------------------------' * 3)
    print(board[6], board[7], board[8])
    print('\n')


def mouse_to_square(mX, mY):
    if mX in range(0, TILE_SIZE):
        sX = 0
    elif mX in range(TILE_SIZE, TILE_SIZE * 2):
        sX = 1
    elif mX in range(TILE_SIZE * 2, TILE_SIZE * 3):
        sX = 2
    else:
        return -1, -1

    if mY in range(0, TILE_SIZE):
        sY = 0
    elif mY in range(TILE_SIZE, TILE_SIZE * 2):
        sY = 1
    elif mY in range(TILE_SIZE * 2, TILE_SIZE * 3):
        sY = 2
    else:
        return -1, -1

    return sX, sY


def coor_to_tile(coor):
    if coor == (0, 0):
        return 0
    elif coor == (1, 0):
        return 1
    elif coor == (2, 0):
        return 2
    elif coor == (0, 1):
        return 3
    elif coor == (1, 1):
        return 4
    elif coor == (2, 1):
        return 5
    elif coor == (0, 2):
        return 6
    elif coor == (1, 2):
        return 7
    elif coor == (2, 2):
        return 8


def get_top(square_data):
    # Returns the index of the top empty place in a square

    for index, i in enumerate(square_data):
        if -1 not in square_data:  # Full row
            return -1

        if i == -1:
            return index


def no_ends(board, hero):
    my_ends = 0
    for square in range(9):

        top_piece = get_top(board[square])
        if top_piece != -1:
            top_piece -= 1

        if top_piece == hero:
            start_height = 6 - board[square].count(-1)

            if 0 in board[square] or 1 in board[square]:
                for end in ends[square]:

                    end_height = 6 - board[end].count(-1)

                    end_top = get_top(board[end])
                    if end_top != -1:
                        end_top -= 1

                    if start_height >= end_height and end_height < 6:
                        my_ends += 1

    if my_ends == 0:
        return True


def double(square, x):
    for i in range(2):
        if square[i] == x and square[i + 1] == x:
            return True


def is_game_over(turn, phase, board):
    # CHECK FOR NO TOPS
    top_piece_indexes = []

    for i in range(9):
        square = board[i]

        top_piece = get_top(square)

        if top_piece != -1:
            top_piece = top_piece - 1

        top_piece_indexes.append(top_piece)

    top_pieces = []

    for i in range(6):
        top = top_piece_indexes[i]

        top_pieces.append(board[i][top])

    if turn == 0 and 0 not in top_pieces and phase == 'move':  # No red tops
        return True
    if turn == 1 and 1 not in top_pieces and phase == 'move':  # No blue tops
        return True

    # CHECK FOR NO ENDS
    if no_ends(board, 0):
        return True
    if no_ends(board, 1):
        return True


def crushed(square, hero):
    # (0, 0, 1), -1, -1, -1
    # 1, 0, (1, 1, 0), -1, -1

    if hero == 0:
        villain = 1
    else:
        villain = 0

    for i in range(6):
        if i <= 3:
            if square[i] == villain and square[i + 1] == villain:
                if square[i + 2] == hero:
                    return True

    return False


# Possible end square for every start square
ends = [
    [1, 3],
    [0, 2, 4],
    [1, 5],
    [0, 4, 6],
    [1, 3, 5, 7],
    [2, 4, 8],
    [3, 7],
    [4, 6, 8],
    [5, 7],
]
