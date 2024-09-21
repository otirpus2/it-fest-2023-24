import pygame
import sys
import random

# Define constants
WIDTH, HEIGHT = 300, 300
ROWS, COLS = 3, 3
SQUARE_SIZE = WIDTH // COLS

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Define the font for displaying the game status
font = pygame.font.SysFont(None, 40)

def draw_grid():
    for x in range(0, WIDTH, SQUARE_SIZE):
        pygame.draw.line(window, BLACK, (x, 0), (x, HEIGHT), 2)
    for y in range(0, HEIGHT, SQUARE_SIZE):
        pygame.draw.line(window, BLACK, (0, y), (WIDTH, y), 2)

def draw_markers(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'X':
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.line(window, BLACK, (x - 30, y - 30), (x + 30, y + 30), 2)
                pygame.draw.line(window, BLACK, (x - 30, y + 30), (x + 30, y - 30), 2)
            elif board[row][col] == 'O':
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(window, BLACK, (x, y), 30, 2)

def get_empty_cells(board):
    empty_cells = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == '-':
                empty_cells.append((row, col))
    return empty_cells

def check_winner(board, marker):
    # Check rows, columns, and diagonals for a winner
    for i in range(ROWS):
        if all(board[i][j] == marker for j in range(COLS)):
            return True
    for j in range(COLS):
        if all(board[i][j] == marker for i in range(ROWS)):
            return True
    if all(board[i][i] == marker for i in range(ROWS)):
        return True
    if all(board[i][ROWS - i - 1] == marker for i in range(ROWS)):
        return True
    return False

def minimax(board, depth, maximizing_player):
    if check_winner(board, 'X'):
        return -10
    if check_winner(board, 'O'):
        return 10
    if len(get_empty_cells(board)) == 0:
        return 0

    if maximizing_player:
        max_eval = -float('inf')
        for row, col in get_empty_cells(board):
            board[row][col] = 'O'
            eval = minimax(board, depth + 1, False)
            board[row][col] = '-'
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for row, col in get_empty_cells(board):
            board[row][col] = 'X'
            eval = minimax(board, depth + 1, True)
            board[row][col] = '-'
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board):
    best_move = None
    best_eval = -float('inf')
    for row, col in get_empty_cells(board):
        board[row][col] = 'O'
        eval = minimax(board, 0, False)
        board[row][col] = '-'
        if eval > best_eval:
            best_eval = eval
            best_move = (row, col)
    return best_move

def main():
    board = [['-' for _ in range(COLS)] for _ in range(ROWS)]
    turn = 'X'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 'X':
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                if board[row][col] == '-':
                    board[row][col] = 'X'
                    turn = 'O'

        if turn == 'O':
            row, col = get_best_move(board)
            if row is not None and col is not None:
                board[row][col] = 'O'
            turn = 'X'

        window.fill(WHITE)
        draw_grid()
        draw_markers(board)

        if check_winner(board, 'X'):
            pygame.time.wait(500)
            window.fill(WHITE)
            draw_grid()
            draw_markers(board)
            text = font.render("You Win!", True, BLACK)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            board = [['-' for _ in range(COLS)] for _ in range(ROWS)]
            turn = 'X'

        if check_winner(board, 'O'):
            pygame.time.wait(500)
            window.fill(WHITE)
            draw_grid()
            draw_markers(board)
            text = font.render("AI Wins!", True, BLACK)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            board = [['-' for _ in range(COLS)] for _ in range(ROWS)]
            turn = 'X'

        if len(get_empty_cells(board)) == 0:
            pygame.time.wait(500)
            window.fill(WHITE)
            draw_grid()
            draw_markers(board)
            text = font.render("It's a Draw!", True, BLACK)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            board = [['-' for _ in range(COLS)] for _ in range(ROWS)]
            turn = 'X'

        pygame.display.update()

if __name__ == "__main__":
    main()
