import pygame
from pygame import Color

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6,6
SQUARE_SIZE = WIDTH/COLS

WHITE = Color(235, 235, 220)               
BLACK = (51, 51, 51)
RED = (178, 34, 34)
BLUE = (25, 25, 112)
MOVABLE_PIECE = Color(255, 165, 0, 20)
SELECTED_PIECE = Color(255, 69, 0, 50)  # Orange red with 50 alpha
VALID_MOVE = Color(135, 206, 250, 100)   # Light sky blue with 100 alpha


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
    # Create a surface for movable pieces highlight
    movable_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    movable_highlight.fill(MOVABLE_PIECE)

    # Draw movable pieces highlight
    for (row, col) in movable_pieces:
        screen.blit(movable_highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Draw selected piece highlight
    if selected_piece:
        row, col = selected_piece
        selected_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        selected_highlight.fill(SELECTED_PIECE)
        screen.blit(selected_highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Draw valid moves highlight
    for (row, col) in valid_move:
        valid_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        valid_highlight.fill(VALID_MOVE)
        screen.blit(valid_highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def get_row_col_from_mouse(pos):
    x ,y = pos
    return int(y//SQUARE_SIZE), int(x//SQUARE_SIZE)

def get_movable_pieces():
    global movable_pieces
    movable_pieces = []
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece == PLAYER_PIECE:
                if row > 0:
                    if col > 0 and board[row - 1][col - 1] == EMPTY:
                        movable_pieces.append((row, col))
                    if col < COLS - 1 and board[row - 1][col + 1] == EMPTY:
                        movable_pieces.append((row, col))


def computerPlay():
    global PLAYER_TURN
    print("Now computer's turn")
    PLAYER_TURN = True
    print("from comPlay, player Turn: ", PLAYER_TURN)
    return



def playerPlay(event):
    global PLAYER_TURN, selected_piece, valid_move, movable_pieces
    print("from player play, turn: ",PLAYER_TURN)

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
                PLAYER_TURN = False  # Switch to computer's turn

            elif piece == PLAYER_PIECE and (row, col) in movable_pieces:
                selected_piece = (row, col)
                valid_move = []
                if row > 0:
                    if col > 0 and board[row - 1][col - 1] == EMPTY:
                        valid_move.append((row - 1, col - 1))
                    if col < COLS - 1 and board[row - 1][col + 1] == EMPTY:
                        valid_move.append((row - 1, col + 1))
                print("Valid moves:", valid_move)
                
            # else:
            #     selected_piece = None
            #     valid_move = []

                
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