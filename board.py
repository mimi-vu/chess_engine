import pygame
import chess 

pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Chess')

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 8, 8
DIMENSION = 8  # Chessboard dimensions
SQUARE_SIZE = 100
COLORS = [(240, 217, 181), (181, 136, 99)]  # Light and dark squares
HIGHLIGHT_COLOR = (97, 97, 164)

board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp"] * 8,
    ["--"] * 8,
    ["--"] * 8,
    ["--"] * 8,
    ["--"] * 8,
    ["wp"] * 8,
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

def draw_board(selected_square=None):
    for row in range(ROWS):
        for col in range(COLS):
            color = COLORS[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Highlight the selected square
            if selected_square:
                selected_row, selected_col, selected_piece = selected_square
                if row == selected_row and col == selected_col:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def load_piece_images():
    piece_images = {}
    pieces = ['bp', 'bn', 'bb', 'br', 'bq', 'bk', 'wp', 'wn', 'wb', 'wr', 'wq', 'wk']
    for piece in pieces:
        image = pygame.image.load(f"images/{piece}.png")
        piece_images[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    return piece_images

def draw_pieces(board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_square_under_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = mouse_y // SQUARE_SIZE
    col = mouse_x // SQUARE_SIZE
    return row, col

def is_valid_move(start, end, piece, board):
    if start == end:
        return False
    start_row, start_col = start
    end_row, end_col = end
    print(start, end)

    if 'w' in piece and 'w' in board[end_row][end_col]:
        return False
    if 'b' in piece and 'wb' != piece and 'b' in board[end_row][end_col] and 'wb' != board[end_row][end_col]:
        return False
    
    if 'p' in piece:
        if (start_row == 6 or start_row == 1) and abs(end_row - start_row) <= 2:
            return True
        elif abs(end_row - start_row) == 1 and abs(end_col - start_col) <= 1:
            return True
    elif 'k' in piece:
        if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1:
            return True
    elif 'b' in piece:
        return False
    elif 'q' in piece:
        return False
    elif 'r' in piece:
        return False
    elif 'n' in piece:
        return False
    return False 


piece_images = load_piece_images()
running = True
turn = "white"
selected_piece = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_under_mouse()

            if selected_piece:
                # Try to move the piece
                start_row, start_col, piece = selected_piece
                if board[start_row][start_col].startswith(turn[0]) and is_valid_move((start_row, start_col), (row, col), piece, board):
                    board[start_row][start_col] = "--"
                    if 'p' in piece:
                        if turn == 'white' and row == 0:
                            piece = "wq"
                        elif turn == 'black' and row == 7:
                            piece = "bq"

                    board[row][col] = piece
                    selected_piece = None
                    # Switch turns
                    turn = "white" if turn == "black" else "black"
                else:
                    selected_piece = None  # Deselect if invalid move
            else:
                # Select the piece if it belongs to the current player
                if board[row][col] != "--" and board[row][col].startswith(turn[0]):
                    selected_piece = (row, col, board[row][col])

    draw_board(selected_square=selected_piece)
    draw_pieces(board)
    pygame.display.flip()
# Quit Pygame
pygame.quit()