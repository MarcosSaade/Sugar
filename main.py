import pygame
from ai import *
from functions import *

repeat_count = repeats


class Main:
    def __init__(self):
        self.board = Board()
        self.mover = Mover()
        self.manager = Manager()

    def start(self):
        self.board.generate_board()

    def update(self):
        self.board.draw_board()
        self.board.generate_pieces()
        self.board.draw_pieces()


class Manager:
    def __init__(self):
        self.ai = True
        self.game_over = False

    def reset(self):
        pygame.time.wait(3000)
        screen.fill((200, 0, 0))
        pygame.display.update()
        pygame.time.wait(500)
        main.mover.turn = 0
        main.mover.r_pieces = 6
        main.mover.b_pieces = 6
        main.board.pieces = []
        main.board.board = [[-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            [-1, -1, -1, -1, -1, -1, ],
                            ]
        main.mover.phase = 'place'


class Board:
    def __init__(self):
        self.tiles = []
        self.pieces = []
        self.borders = []
        self.colors = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        self.board = initial_board

    def generate_board(self):
        for i in range(3):
            for j in range(3):
                self.tiles.append(pygame.rect.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_board(self):
        for index, i in enumerate(self.tiles):
            if index % 2 == 0:
                color = GRAY_1
            else:
                color = GRAY_2

            pygame.draw.rect(screen, color, i)

    def generate_pieces(self):
        for num, square in enumerate(main.board.board):
            for index, stack in enumerate(square):
                if stack != -1:
                    if num in [0, 1, 2]:
                        x = num
                        y = 1
                    elif num in [3, 4, 5]:
                        x = num - 3
                        y = 200
                    else:
                        x = num - 6
                        y = 400

                    left = (x * TILE_SIZE) + (TILE_SIZE * 0.4)
                    top = y + (TILE_SIZE * 0.6) - (index * 6)

                    piece = pygame.rect.Rect(left, top, 80, 30)

                    if piece not in self.pieces:
                        self.pieces.append(piece)

    def draw_pieces(self):
        pieces = []

        for i in range(9):
            for j in main.board.board[i]:
                if j != -1:
                    pieces.append(j)

        for index, i in enumerate(self.pieces):
            if pieces[index] == 0:  # red
                pygame.draw.rect(screen, reds[self.colors[index]], i)
            else:  # blue
                pygame.draw.rect(screen, blues[self.colors[index]], i)


class Mover:
    def __init__(self):
        self.r_pieces = 6
        self.b_pieces = 6

        self.last_move = -1

        self.turn = 0

        self.phase = 'place'

        self.clicks = []

    def place(self, coor):
        if self.turn == 0:
            tile = coor_to_tile(coor)

            square_data = main.board.board[tile]

            if get_top(square_data) == -1:
                return
            else:
                top = get_top(square_data)

            main.board.board[tile][top] = 0

            self.last_move = tile

            self.r_pieces -= 1

            self.turn = 1

        else:
            if self.b_pieces > 0:
                if main.manager.ai:
                    tile = generate_move('place', main.board.board, self.r_pieces + 1, self.last_move, False)
                    square_data = main.board.board[tile]
                    top = get_top(square_data)
                else:
                    tile = coor_to_tile(coor)
                    square_data = main.board.board[tile]

                    if get_top(square_data) == -1:
                        self.move(main.manager.ai)
                        return
                    else:
                        top = get_top(square_data)

                main.board.board[tile][top] = 1

                self.b_pieces -= 1

                self.turn = 0

        # Generate piece graphics again
        main.board.pieces = []
        main.board.generate_pieces()

    def move(self, ai):
        if ai:
            start, end = generate_move('move', main.board.board, 8, self.last_move, False)
            self.last_move = start, end

            if start == -1 and end == -1:
                main.manager.reset()
                return
        else:
            start = coor_to_tile(self.clicks[0])
            end = coor_to_tile(self.clicks[1])

        # Can't move unto itself
        if start == end:
            return

        # Can't move to a higher tower
        len_start = main.board.board[start].count(1) + main.board.board[start].count(0)
        len_end = main.board.board[end].count(1) + main.board.board[end].count(0)

        if len_start < len_end:
            return

        # Only move to adjacent squares (no diagonal movements allowed)
        if start == 0:
            if end not in [1, 3]:
                return
        elif start == 1:
            if end not in [0, 2, 4]:
                return
        elif start == 2:
            if end not in [1, 5]:
                return
        elif start == 3:
            if end not in [0, 4, 6]:
                return
        elif start == 4:
            if end not in [1, 3, 5, 7]:
                return
        elif start == 5:
            if end not in [2, 4, 8]:
                return
        elif start == 6:
            if end not in [3, 7]:
                return
        elif start == 7:
            if end not in [4, 6, 8]:
                return
        elif start == 8:
            if end not in [5, 7]:
                return

        # Get the index of the topmost piece
        top_piece = get_top(main.board.board[start])
        if top_piece != -1:
            top_piece = top_piece - 1  # We want the top piece, not the top space

        color = main.board.board[start][top_piece]  # Which color is moving

        # Move by turns
        if color != self.turn:
            return

        # get available space at end
        square_data = main.board.board[end]

        if get_top(square_data) == -1:
            return
        else:
            top_end = get_top(square_data)

        main.board.board[start][top_piece] = -1  # remove piece from start
        main.board.board[end][top_end] = color

        # Switch turn
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

        # Generate piece graphics again
        main.board.pieces = []
        main.board.generate_pieces()


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse = pygame.mouse.get_pos()
            coor = mouse_to_square(mouse[0], mouse[1])

            if main.mover.r_pieces == 0 and main.mover.b_pieces == 0 and main.mover.phase == 'place':
                main.mover.phase = 'move'

            if main.mover.phase == 'place':
                if coor != (-1, -1):
                    if main.manager.ai:
                        main.mover.place(coor)
                        main.mover.place(coor)
                    else:
                        main.mover.place(coor)

            else:  # Move phase
                if len(main.mover.clicks) == 2:
                    main.mover.clicks = []

                main.mover.clicks.append(coor)

                if main.board.board[coor_to_tile(coor)] == [-1, -1, -1, -1, -1, -1] and len(main.mover.clicks) == 1:
                    main.mover.clicks = []

                if len(main.mover.clicks) == 2:
                    if main.manager.ai:
                        main.mover.move(False)
                        main.mover.move(True)
                    else:
                        main.mover.move(False)

        if event.type == pygame.KEYDOWN:
            print_board(main.board.board)


clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

main = Main()
main.start()

while True:
    screen.fill((0, 0, 0))
    events()
    main.update()
    pygame.display.update()
    clock.tick(FPS)
