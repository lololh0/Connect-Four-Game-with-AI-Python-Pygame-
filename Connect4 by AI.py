import sys
import random
import math
import pygame

TRANSPARENT = (0, 0, 0, 0)
GLASS_BLUE = (84, 153, 199, 150)
GLASS_RED = (255, 99, 132, 150)
GLASS_YELLOW = (255, 200, 77, 150)
GLASS_WHITE = (255, 255, 255, 150)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
    return [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r

def print_board(board):
    for row in board:
        print(row)

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, GLASS_BLUE, (c * 100, r * 100 + 100, 100, 100))
            pygame.draw.circle(screen, TRANSPARENT, (int(c * 100 + 100 / 2), int(r * 100 + 100 + 100 / 2)), 45)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, GLASS_RED, (int(c * 100 + 100 / 2), 700 - int(r * 100 + 100 / 2)), 45)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, GLASS_YELLOW, (int(c * 100 + 100 / 2), 700 - int(r * 100 + 100 / 2)), 45)
    pygame.display.update()

pygame.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")

myfont = pygame.font.SysFont("monospace", 75)

board = create_board()
game_over = False

turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, TRANSPARENT, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, GLASS_RED, (posx, int(SQUARESIZE / 2)), 45)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, TRANSPARENT, (0, 0, width, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("you won!!", 1, GLASS_WHITE)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn %= 2

                    draw_board(board)

    if turn == AI and not game_over:
        col = random.randint(0, COLUMN_COUNT - 1)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("you lost!!", 1, GLASS_WHITE)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(board)

            turn += 1
            turn %= 2

    if game_over:
        pygame.time.wait(3000)
