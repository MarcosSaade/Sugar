import random
from functions import *
from settings import repeats

repeat_count = repeats


def generate_move(phase, board, depth, last_move, maximizer):
    global repeat_count

    if maximizer:
        ai_color = 0
    else:
        ai_color = 1

    if phase == 'place':
        best_score = math.inf

        for square in range(9):
            top_space = get_top(board[square])

            if board[square][top_space] == -1:  # if move is legal

                if square == last_move:
                    repeat_count += 1

                board[square][top_space] = ai_color  # make move
                score = minimax(board, depth, -math.inf, math.inf, maximizer, phase)  # call minimax
                board[square][top_space] = -1  # unmake move

                if repeat_count <= 3:
                    if score < best_score:
                        best_score = score
                        best_move = square

                else:
                    if score < best_score and square != last_move:
                        best_score = score
                        best_move = square

        return best_move

    else:  # Move phase
        best_score = math.inf
        best_move = -1, -1

        my_squares = []

        # Look for legal moves
        for square in range(9):
            top_piece = get_top(board[square])
            if top_piece != -1:
                top_piece = top_piece - 1

            if board[square][top_piece] == ai_color:
                my_squares.append(square)

        if len(my_squares) == 0:  # It has lost, no possible moves available
            print('game over no tops')
            return -1, -1

        for square in my_squares:
            start_piece = get_top(board[square])  # Piece which is moving
            if start_piece != -1:
                start_piece = start_piece - 1

            possible_ends = ends[square]

            for i in range(len(possible_ends)):  # Check each possible end for each piece
                start_height = 6 - board[square].count(-1)
                end_height = 6 - board[ends[square][i]].count(-1)

                if start_height >= end_height:  # If target is equal or lower in height
                    end = ends[square][i]
                    end_space = get_top(board[end])  # Moving to here

                    # Prevent repetition
                    if ((end, square) != last_move) or ((end, square) == last_move and random.randint(0, 2) == 0):

                        # CHOOSING A MOVE
                        # Make move
                        board[square][start_piece] = -1
                        board[end][end_space] = ai_color

                        # Call Minimax
                        score = minimax(board, depth, -math.inf, math.inf, False, phase)

                        # Unmake move
                        board[square][start_piece] = ai_color
                        board[end][end_space] = -1

                        if score < best_score:
                            best_score = score
                            best_move = square, end

        print(f'eval: {best_score}')
        return best_move


def minimax(current_board, depth, alpha, beta, maximizing_player, phase):
    if phase == 'place':
        r_pieces = 0
        b_pieces = 0

        if maximizing_player:
            turn = 0
        else:
            turn = 1

        # Check end of depth
        if depth == 0:
            return static_eval(current_board)

        # Check terminal node
        if is_game_over(turn, phase, current_board):
            return static_eval(current_board)

        # Check end of place phase
        for square in current_board:
            r_pieces += square.count(0)
            b_pieces += square.count(1)
        if r_pieces > 6 and b_pieces > 6:
            return static_eval(current_board)

        if maximizing_player:
            best_score = -math.inf

            for square in range(9):
                top_space = get_top(current_board[square])

                if current_board[square][top_space] == -1:  # if move is legal

                    current_board[square][top_space] = turn  # make move
                    score = minimax(current_board, depth - 1, alpha, beta, False, phase)  # evaluate move
                    current_board[square][top_space] = -1  # unmake move

                    best_score = max(score, best_score)

                    # Alpha Beta pruning
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break

            return best_score

        else:
            best_score = math.inf

            for square in range(9):
                top_space = get_top(current_board[square])

                if current_board[square][top_space] == -1:  # if move is legal

                    current_board[square][top_space] = turn  # make move
                    score = minimax(current_board, depth - 1, alpha, beta, True, phase)  # evaluate move
                    current_board[square][top_space] = -1  # unmake move

                    best_score = min(score, best_score)

                    beta = min(beta, score)
                    if beta <= alpha:
                        break

            return best_score

    elif phase == 'move':
        if maximizing_player:
            turn = 0
        else:
            turn = 1

        # Check end of depth
        if depth == 0:
            return static_eval(current_board)

        # Check terminal node
        if is_game_over(turn, phase, current_board):
            return static_eval(current_board)

        if maximizing_player:
            best_score = -math.inf

            my_squares = []

            # Look for legal moves
            for square in range(9):
                top_piece = get_top(current_board[square])
                if top_piece != -1:
                    top_piece = top_piece - 1

                if current_board[square][top_piece] == 0:
                    my_squares.append(square)

            for square in my_squares:
                start_piece = get_top(current_board[square])  # Piece which is moving

                if start_piece != -1:
                    start_piece = start_piece - 1

                possible_ends = ends[square]

                # Check possible moves
                for i in range(len(possible_ends)):

                    end = ends[square][i]

                    start_height = 6 - (current_board[square]).count(-1)
                    end_height = 6 - (current_board[end]).count(-1)

                    if end_height < 6 and end_height < start_height:
                        end_space = get_top(current_board[end])

                        # Make move
                        current_board[square][start_piece] = -1
                        current_board[end][end_space] = 0

                        # Evaluate move
                        score = minimax(current_board, depth - 1, alpha, beta, False, phase)

                        # Unmake move
                        current_board[square][start_piece] = 0
                        current_board[end][end_space] = -1

                        if score != math.inf:
                            best_score = max(score, best_score)

                        # Alpha Beta pruning
                        alpha = max(alpha, score)

                        if beta <= alpha:
                            break

            return best_score

        else:
            best_score = math.inf

            my_squares = []

            for square in range(9):
                top_piece = get_top(current_board[square])
                if top_piece != -1:
                    top_piece = top_piece - 1

                if current_board[square][top_piece] == 1:
                    my_squares.append(square)

            for square in my_squares:
                start_piece = get_top(current_board[square])

                if start_piece != -1:
                    start_piece = start_piece - 1

                possible_ends = ends[square]

                for i in range(len(possible_ends)):

                    end = ends[square][i]

                    start_height = 6 - (current_board[square]).count(-1)
                    end_height = 6 - (current_board[end]).count(-1)

                    if end_height < 6 and end_height < start_height:
                        end_space = get_top(current_board[end])

                        current_board[square][start_piece] = -1
                        current_board[end][end_space] = 1

                        score = minimax(current_board, depth - 1, alpha, beta, True, phase)

                        current_board[square][start_piece] = 1
                        current_board[end][end_space] = -1

                        if score != -math.inf:
                            best_score = min(score, best_score)

                        # Alpha Beta pruning
                        beta = min(beta, score)
                        if beta <= alpha:
                            break

            return best_score


def static_eval(board):
    score = 0
    tops = []

    for square in range(9):
        top_piece = get_top(board[square])
        if top_piece != -1:
            top_piece = top_piece - 1

        tops.append(board[square][top_piece])

        #  Having the top of a square
        height = 6 - board[square].count(-1)

        if board[square][top_piece] == 0:
            score += height

            # Weight for sides
            if square in [1, 3, 5, 7]:
                score = score * 1.2

            # Weight for center
            if square == 4:
                score = score * 2

        elif board[square][top_piece] == 1:
            score -= height

            # Weight for sides
            if square in [1, 3, 5, 7]:
                score = score * 1.2

            # Weight for center
            if square == 4:
                score = score * 2

        if crushed(board[square], 0):
            score += 30
        if crushed(board[square], 1):
            score -= 30

        # Having doubles that can be easily crushed
        # TODO instead of checking for height x, chek if neighboring squares are higher

        if height <= 3:
            if double(board[square], 1):
                score += 120
            elif double(board[square], 0):
                score -= 120

    if tops.count(1) == 1:
        score += 200
    if tops.count(0) == 1:
        score -= 200

    if 1 not in tops:
        score += 9999
    if 0 not in tops:
        score -= 9999

    # Check for trapped pieces
    for square in [0, 2, 6, 8]:
        h_corner = 6 - board[square].count(-1)

        top_corner = get_top(board[square])
        if top_corner != -1:
            top_corner = top_corner - 1

        piece_corner = board[square][top_corner]

        if square == 0:
            h_1 = 6 - board[square + 1].count(-1)
            h_2 = 6 - board[square + 3].count(-1)

            top_1 = get_top(board[square + 1])
            if top_1 != -1:
                top_1 = top_1 - 1
            top_2 = get_top(board[square + 3])
            if top_2 != -1:
                top_2 = top_1 - 1

            blocker_1 = board[square + 1][top_1]
            blocker_2 = board[square + 3][top_2]

        elif square == 2:
            h_1 = 6 - board[square - 1].count(-1)
            h_2 = 6 - board[square + 3].count(-1)

            top_1 = get_top(board[square - 1])
            if top_1 != -1:
                top_1 = top_1 - 1
            top_2 = get_top(board[square + 3])
            if top_2 != -1:
                top_2 = top_2 - 1

            blocker_1 = board[square - 1][top_1]
            blocker_2 = board[square + 3][top_2]

        elif square == 6:
            h_1 = 6 - board[square + 1].count(-1)
            h_2 = 6 - board[square - 3].count(-1)

            top_1 = get_top(board[square + 1])
            if top_1 != -1:
                top_1 = top_1 - 1
            top_2 = get_top(board[square - 3])
            if top_2 != -1:
                top_2 = top_2 - 1

            blocker_1 = board[square + 1][top_1]
            blocker_2 = board[square - 3][top_2]

        elif square == 8:
            h_1 = 6 - board[square - 1].count(-1)
            h_2 = 6 - board[square - 3].count(-1)

            top_1 = get_top(board[square - 1])
            if top_1 != -1:
                top_1 = top_1 - 1
            top_2 = get_top(board[square - 3])
            if top_2 != -1:
                top_2 = top_2 - 1

            blocker_1 = board[square - 1][top_1]
            blocker_2 = board[square - 3][top_2]

        if h_corner < h_1 and h_corner < h_2:
            if piece_corner == 1 and blocker_1 == 0 and blocker_2 == 0:
                score += 70

                # Player 0 has won
                if tops.count(1) == 1:
                    score = score * 999

            elif piece_corner == 0 and blocker_1 == 1 and blocker_2 == 1:
                score - 70

                if tops.count(0) == 1:
                    score = score * 999

    return round(score)
