import pygame
from pygame import Color

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 6, 6
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = Color(235, 235, 220)
BLACK = (51, 51, 51)
RED = (178, 34, 34)
BLUE = (25, 25, 112)
MOVABLE_PIECE = Color(255, 165, 0, 20)
SELECTED_PIECE = Color(255, 69, 0, 50)
VALID_MOVE = Color(135, 206, 250, 100)
BACKGROUND_GRADIENT = (0, 0, 255)  # Blue gradient

# Piece representation
EMPTY = 0
COM_PIECE = 1
PLAYER_PIECE = 2
COM_KING = 3
PLAYER_KING = 4

# Initialize the board
board = [
    [EMPTY, COM_PIECE, EMPTY, COM_PIECE, EMPTY, COM_PIECE],
    [COM_PIECE, EMPTY, COM_PIECE, EMPTY, COM_PIECE, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [PLAYER_PIECE, EMPTY, PLAYER_PIECE, EMPTY, PLAYER_PIECE, EMPTY],
    [EMPTY, PLAYER_PIECE, EMPTY, PLAYER_PIECE, EMPTY, PLAYER_PIECE]
]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Checkers")

# Game variables
PLAYER_TURN = True
selected_piece = None
movable_pieces = []
valid_move = []

# Draw gradient background
def draw_gradient_background():
    for y in range(HEIGHT):
        color = (int(255 * (y / HEIGHT)), int(255 * (y / HEIGHT)), 255)  # Blue gradient
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

# Draw the board
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces with shadows
def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != EMPTY:
                # Draw shadow
                shadow_offset = 5
                shadow_color = (0, 0, 0, 100)
                pygame.draw.circle(screen, shadow_color, (col * SQUARE_SIZE + SQUARE_SIZE // 2 + shadow_offset, row * SQUARE_SIZE + SQUARE_SIZE // 2 + shadow_offset), SQUARE_SIZE // 3)

                # Draw piece
                if piece == COM_PIECE or piece == COM_KING:
                    color = RED
                elif piece == PLAYER_PIECE or piece == PLAYER_KING:
                    color = BLUE
                pygame.draw.circle(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

# Draw highlights for movable pieces, selected piece, and valid moves
def draw_highlights():
    # Movable pieces
    movable_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    movable_highlight.fill(MOVABLE_PIECE)
    for (row, col) in movable_pieces:
        screen.blit(movable_highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Selected piece
    if selected_piece:
        row, col = selected_piece
        selected_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        selected_highlight.fill(SELECTED_PIECE)
        screen.blit(selected_highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Valid moves
    for (row, col) in valid_move:
        valid_highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        valid_highlight.fill(VALID_MOVE)
        screen.blit(valid_highlight, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Get row and column from mouse position
def get_row_col_from_mouse(pos):
    x, y = pos
    return int(y // SQUARE_SIZE), int(x // SQUARE_SIZE)

# Get movable pieces for the player
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

# Handle player moves
def playerPlay(event):
    global PLAYER_TURN, selected_piece, valid_move
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = get_row_col_from_mouse(pos)
        piece = board[row][col]

        if selected_piece:
            if (row, col) in valid_move:
                board[row][col] = board[selected_piece[0]][selected_piece[1]]
                board[selected_piece[0]][selected_piece[1]] = EMPTY
                selected_piece = None
                valid_move = []
                PLAYER_TURN = False
        else:
            if piece == PLAYER_PIECE and (row, col) in movable_pieces:
                selected_piece = (row, col)
                valid_move = []
                if row > 0:
                    if col > 0 and board[row - 1][col - 1] == EMPTY:
                        valid_move.append((row - 1, col - 1))
                    if col < COLS - 1 and board[row - 1][col + 1] == EMPTY:
                        valid_move.append((row - 1, col + 1))

# Handle computer moves (placeholder)
def computerPlay():
    global PLAYER_TURN
    print("Computer's turn")
    PLAYER_TURN = True

# Main game loop
def main():
    global PLAYER_TURN
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if PLAYER_TURN:
                playerPlay(event)
            else:
                computerPlay()

        draw_gradient_background()
        draw_board()
        draw_pieces()
        get_movable_pieces()
        draw_highlights()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()