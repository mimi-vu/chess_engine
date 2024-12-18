import pygame

pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Chess')

WIDTH, HEIGHT = 400, 400
ROWS, COLS = 8, 8
DIMENSION = 8  # Chessboard dimensions
SQUARE_SIZE = 50
COLORS = [(240, 217, 181), (181, 136, 99)]  # Light and dark squares
HIGHLIGHT_COLOR = (97, 97, 164)

# Set up the board in a 8x8 matrix
board = [
    ["bru", "bn", "bb", "bq", "bku", "bb", "bn", "bru"],
    ["bp"] * 8,
    ["--"] * 8,
    ["--"] * 8,
    ["--"] * 8,
    ["--"] * 8,
    ["wp"] * 8,
    ["wru", "wn", "wb", "wq", "wku", "wb", "wn", "wru"]
]

# Store the positions of each piece and what type of piece they are
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_pieces_locations = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                          (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_pieces_locations = [(7, 7), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
                          (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]

# This determines whether pieces can attack through pieces no matter if its an enemy or a friendly
phasing = False
pawn_move_2_spaces = False # boolean
pawn_moved_2_spaces = None # coordinates

def check_enpassant(end):
    end_row, end_col = end
    pawn_row, pawn_col = pawn_moved_2_spaces; 
    if abs(end_col - pawn_col) == 1 and end_row == pawn_row:
        return True
    return False

# Does the background of the board
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

# Load the images to be used later
def load_piece_images():
    piece_images = {}
    pieces = ['bp', 'bpp', 'bn', 'bb', 'br', 'bru', 'bq', 'bk', 'bku', 'wp', 'wpe', 'wn', 'wb', 'wr', 'wru', 'wq', 'wk', 'wku']
    for piece in pieces:
        image = pygame.image.load(f"assets/{piece}.png")
        piece_images[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    return piece_images

# Draws the pieces onto the board
def draw_pieces(board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "--":
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Returns the coordinates of where the mouse is
def get_square_under_mouse():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row = mouse_y // SQUARE_SIZE
    col = mouse_x // SQUARE_SIZE
    return row, col

# Checks if a piece can move from the start to the end diagonally
def check_diagonal(start, end):
    start_row, start_col = start
    end_row, end_col = end

    if abs(end_row - start_row) == abs(end_col - start_col) and abs(end_row - start_row) != 0:
        if phasing:
            return True
        
        # This chunk of code is to determine what diagonal the piece is going e.g. left upwards
        row_increment = 1
        col_increment = 1
        if start_row > end_row:
            row_increment = -1
        if start_col > end_col:
            col_increment = -1
        
        # Continues along the diagonal and ensures that no piece is blocking the path
        while start_row > -1 and start_row < 8 and start_row != end_row and start_col > -1 and start_col < 8 and start_col != end_col:
            start_row += row_increment
            start_col += col_increment
            
            # If a piece is blocking its path then exit out of the loop
            if board[start_row][start_col] != '--':
                break
        
        # If it reaches the end goal then nothing is wrong with the piece moving so it moves
        if start_row == end_row and start_col == end_col:
            return True
        
    # Piece does not move
    return False

def check_horizontal(start, end):
    start_row, start_col = start
    end_row, end_col = end
    
    if end_row - start_row == 0:
        if phasing:
            return True
        
        # Determines the direction the piece is going e.g. left/right
        col_increment = 1
        if start_col > end_col:
            col_increment = -1

        while start_col > -1 and start_col < 8 and start_col != end_col:
            start_col += col_increment

            # A piece may be blocking its path so exit out of the loop
            if board[start_row][start_col] != '--':
                break
        
        # Lets the piece move if it reached the end goal
        if start_col == end_col:
            return True
    return False

def check_vertical(start, end):
    start_row, start_col = start
    end_row, end_col = end
    
    if end_col - start_col == 0:
        if phasing:
            return True
        
        # Determines the direction the piece is going e.g. up/down
        row_increment = 1
        if start_row > end_row:
            row_increment = -1
        
        while start_row > -1 and start_row < 8 and start_row != end_row:
            start_row += row_increment
            
            # A piece may be blocking its path so exit out of the loop
            if board[start_row][start_col] != '--':
                break
        
        # Lets the piece move if it reached the end goal
        if start_row == end_row:
            return True
    return False

def is_valid_move(start, end, piece, board):
    # If the piece isn't moving, don't let the piece move lol
    if start == end:
        return False
    
    start_row, start_col = start # (row, col)
    end_row, end_col = end

    # Stops the piece from taking its own team
    if piece.startswith('w') and board[end_row][end_col].startswith('w'):
        return False
    if piece.startswith('b') and board[end_row][end_col].startswith('b'):
        return False
    
    # Move checking for pawns
    if piece.endswith('p'):
        # If the pawn is moving way too far to the side, don't allow it
        if abs(end_col - start_col) > 1:
            return False
        
        # This allows a pawn to move 2 spaces forward when it is at its starting rank
        if (start_row == 6 or start_row == 1) and abs(end_row - start_row) <= 2:
            # store enpassatable
            pawn_moved_2_spaces = (end_row, end_col)
            return True
        
        # If the pawn is moving 1 space check out these cases
        elif abs(end_row - start_row) == 1:

            # If it is moving forward check if a piece is blocking its way
            if (end_col - start_col) == 0 and board[end_row][end_col] != '--':
                return False
            
            # If it is moving diagonally upwards check if it is taking a piece
            if abs(end_col - start_col) == 1:
                # enpassanting 
                if pawn_moved_2_spaces and check_enpassant(end):
                    pawn_row, pawn_col = pawn_moved_2_spaces
                    board[pawn_row][pawn_col] = '--'
                    return True
                
                if piece.startswith('w'):
                    return board[end_row][end_col].startswith('b')
                if piece.startswith('b'):
                    return board[end_row][end_col].startswith('w')
            
            # If its a white pawn check if it is moving upward, downwards for black pawns
            if piece.startswith('w') and (end_row - start_row) == -1:
                return True
            if piece.startswith('b') and (end_row - start_row) == 1:
                return True
            
    # Move checking for kings
    elif 'k' in piece:
        # Check castling (very rough version doesn't check if there are checks)
        # Checks kingside castling
        if end_col - start_col == 2 and 'u' in piece and 'u' in board[start_row][7]:
            col_increment = 1
            while start_col < 8 and start_col != end_col:
                start_col += col_increment
                if board[start_row][start_col] != '--':
                    return False
            
            rook = board[start_row][7]
            board[start_row][7] = '--'
            board[start_row][end_col - 1] = rook
            return True
        
        # Checks queenside castling
        if end_col - start_col == -2 and 'u' in piece and 'u' in board[start_row][0]:
            col_increment = -1
            while start_col > -1 and start_col != end_col:
                start_col += col_increment
                if board[start_row][start_col] != '--':
                    return False
            
            rook = board[start_row][0]
            board[start_row][0] = '--'
            board[start_row][end_col + 1] = rook
            return True
                    
        # As long as it is moving inbetween a 3x3 square centred around the king it can move
        if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1:
            return True
    
    # Move checking for bishops
    elif piece.endswith('b'):
        # Check diagonal returns a boolean on whether it can move diagonally 
        return check_diagonal(start, end)
    
    # Move checking for queens
    elif piece.endswith('q'):
        # Since a queen can move horizontally, vertically or diagonally if any of these are true then it can move that way 
        return check_diagonal(start, end) or check_horizontal(start, end) or check_vertical(start, end)
    
    # Move checking for rooks
    elif 'r' in piece:
        # Check horizontal and vertical directions if any is true it can move
        return check_horizontal(start, end) or check_vertical(start, end)
    
    # Move checking for knights
    elif piece.endswith('n'):
        # This checks if the knight moves upwards/downwards 2 spaces then to the left/right 1 space
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1:
            return True
        # This checks if the knight moves upwards/downwards 1 space then to the left/right 2 spaces
        if abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2:
            return True
    # If the piece somehow doesn't exist then it will not move, though how the code got here is beyond me
    return False 

piece_images = load_piece_images()
running = True
turn = "white"
selected_piece = None

# Infinite loop while game is running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_under_mouse()

            if selected_piece:
                # Separates the variables 
                start_row, start_col, piece = selected_piece

                # Checks if that piece is a piece of the current players, then checks if the move is a valid move
                if board[start_row][start_col].startswith(turn[0]) and is_valid_move((start_row, start_col), (row, col), piece, board):

                    if pawn_move_2_spaces:
                        piece = turn[0] + 'pe'
                        pawn_move_2_spaces = False
                    elif pawn_moved_2_spaces:
                        pawn_moved_2_spaces = None
                    # Sets the original spot to be empty
                    board[start_row][start_col] = "--"

                    # Promotes the piece to be a queen when it reaches the end
                    if 'p' in piece:
                        if turn == 'white' and row == 0:
                            piece = "wq"
                        elif turn == 'black' and row == 7:
                            piece = "bq"
                    
                    # If the piece hasn't been moved yet but is moving this turn update it so it doesn't have the tag that it hasn't moved
                    # This is for castling checks
                    if 'u' in piece:
                        if 'k' in piece:
                            piece = turn[0] + 'k'
                        if 'r' in piece:
                            piece = turn[0] + 'r'

                    # Sets the new spot to have the piece
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
    pygame.display.update()

# Quit Pygame
pygame.quit()