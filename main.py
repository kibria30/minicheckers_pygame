import pygame
from pygame import Color
from minimax import Minimax
import copy

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6,6
SQUARE_SIZE = WIDTH/COLS

WHITE = (235, 235, 220)               
BLACK = (51, 51, 51)
RED = (178, 34, 34)
BLUE = (25, 25, 185)
MOVABLE_PIECE = (0, 200, 0, 100)
SELECTED_PIECE = (255, 255, 0, 50)
VALID_MOVE = Color(155, 215, 255, 100) 


EMPTY = 0
COM_PIECE = 1
PLAYER_PIECE = 2
COM_KING = 3
PLAYER_KING = 4

board = [
    [EMPTY, COM_PIECE, EMPTY, COM_PIECE, EMPTY, COM_PIECE],
    [COM_PIECE, EMPTY, COM_PIECE, EMPTY, COM_PIECE, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, PLAYER_PIECE, EMPTY, PLAYER_PIECE, EMPTY, PLAYER_PIECE],
    [PLAYER_PIECE, EMPTY, PLAYER_PIECE, EMPTY, PLAYER_PIECE, EMPTY]
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini checkers")

PLAYER_TURN = True
selected_piece = None
movable_pieces = []
valid_move = []

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = BLACK if (row+col)%2 else WHITE
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != EMPTY:
                if piece == COM_PIECE:
                    color = RED
                elif piece == PLAYER_PIECE:
                    color = BLUE
                pygame.draw.circle(screen, color, [col*SQUARE_SIZE+(SQUARE_SIZE//2), row*SQUARE_SIZE+(SQUARE_SIZE//2)], SQUARE_SIZE//3)               
                # if piece == COM_KING or piece == PLAYER_KING:
                #     pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)

# def draw_king():
#     pygame.draw.polygon(screen, (0, 255, 0), [[15, 75], [25,50], [35,62], [45, 37], [55,62], [65, 50], [75, 75]])

def draw_highlights():
    # Draw movable pieces highlight (hollow circle)
    for (row, col) in movable_pieces:
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 3 + 3
        pygame.draw.circle(screen, MOVABLE_PIECE, (x, y), radius, width=3)  # Hollow circle

    # Draw selected piece highlight (hollow circle)
    if selected_piece:
        row, col = selected_piece
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        radius = SQUARE_SIZE // 3 + 3
        pygame.draw.circle(screen, SELECTED_PIECE, (x, y), radius, width=3)  # Hollow circle

    for (row, col) in valid_move:
        radius = SQUARE_SIZE // 3  # Smaller than a piece
        valid_move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(valid_move_surface, VALID_MOVE, (SQUARE_SIZE//2, SQUARE_SIZE//2), radius)
        screen.blit(valid_move_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_row_col_from_mouse(pos):
    x ,y = pos
    return int(y//SQUARE_SIZE), int(x//SQUARE_SIZE)

def get_movable_pieces():
    global movable_pieces
    movable_pieces = []
    movable_pieces_set = set()
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece == PLAYER_PIECE:
                if row > 0:
                    if col > 0 and board[row - 1][col - 1] == EMPTY:
                        movable_pieces_set.add((row, col))
                    if col < COLS - 1 and board[row - 1][col + 1] == EMPTY:
                        movable_pieces_set.add((row, col))
    movable_pieces = list(movable_pieces_set)


def computerPlay():
    global PLAYER_TURN

    engine = Minimax(3)
    engine.minimax(board=copy.deepcopy(board), com_turn=True)
    bestMove = engine.best_move

    # if bestMove is None:
    #     print("No valid moves for computer")
    #     PLAYER_TURN = True
    #     return

    board[bestMove[2]][bestMove[3]] = board[bestMove[0]][bestMove[1]]
    board[bestMove[0]][bestMove[1]] = EMPTY
    PLAYER_TURN = True



def playerPlay(event):
    global PLAYER_TURN, selected_piece, valid_move, movable_pieces

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        print(row, col)
        piece = board[row][col]
        if selected_piece:
            if (row, col) in valid_move:
                board[row][col] = board[selected_piece[0]][selected_piece[1]]
                board[selected_piece[0]][selected_piece[1]] = EMPTY
                selected_piece = None
                valid_move = []
                PLAYER_TURN = False
            elif piece == PLAYER_PIECE and (row, col) in movable_pieces:
                selected_piece = (row, col)
                valid_move = []
                if row > 0:
                    if col > 0 and board[row - 1][col - 1] == EMPTY:
                        valid_move.append((row - 1, col - 1))
                    if col < COLS - 1 and board[row - 1][col + 1] == EMPTY:
                        valid_move.append((row - 1, col + 1))
                print("Valid moves:", valid_move)

                
        else:
            if piece == PLAYER_PIECE and (row, col) in movable_pieces:
                selected_piece = (row, col)
                valid_move = []
                if row > 0:
                    if col > 0 and board[row - 1][col - 1] == EMPTY:
                        valid_move.append((row - 1, col - 1))
                    if col < COLS - 1 and board[row - 1][col + 1] == EMPTY:
                        valid_move.append((row - 1, col + 1))
                print("Valid moves:", valid_move)


def main():
    global PLAYER_TURN, movable_pieces
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if PLAYER_TURN:
                playerPlay(event)
                
            else:
                computerPlay()            


        draw_board()
        draw_pieces()
        # draw_king()
        get_movable_pieces()
        draw_highlights()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()