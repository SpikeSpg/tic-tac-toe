import pygame
import sys

pygame.init()

# create a 2d screen
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED =  (255, 100, 100)
BOX_COLOR = (210, 224, 251)

# define position
SPOT = None

# keep track of the moves
player = 'X'
board = [' ' for i in range(9)]

# Create separate surfaces for drawing
surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

def create_board():
    global SPOT
    # background color of the main screen
    screen.fill((249, 243, 204))

    # draw rectangle
    box_x = 375
    box_y = 375
    x = (screen_width - box_x) // 2
    y = (screen_height - box_y) // 2
    pygame.draw.rect(screen, BOX_COLOR, pygame.Rect(x, y, box_x, box_y))

    # create a game table
    lines_color = (142, 172, 205)
    spot_x = (box_x - (12 * 2)) / 3 - 1
    spot_y = (box_y - (12 * 2)) / 3 - 1
    margin = 0
    # horizontal (they're align on the vertical)
    pygame.draw.line(screen, lines_color, (x + margin, y + spot_y + 6), (x + 374 - margin, y + spot_y + 6), 11)
    pygame.draw.line(screen, lines_color, (x + margin, y + (spot_y * 2) + 12 + 6), (x + 374 - margin, y + (spot_y * 2) + 12 + 6), 11)
    # vertical (they're align on the horizontal)
    pygame.draw.line(screen, lines_color, (x + spot_x + 6, y + margin), (x + spot_x + 6, y + 374 - margin), 11)
    pygame.draw.line(screen, lines_color, (x + (spot_x * 2) + 12 + 6, y + margin), (x + (spot_x * 2) + 12 + 6, y + 374 - margin), 11)

    # store all the spot positions
    i0 = ((x, x + spot_x), (y, y + spot_y))
    i1 = ((x + spot_x + 12, x + spot_x * 2 + 12), (y, y + spot_y))
    i2 = ((x + spot_x * 2 + 24, x + spot_x * 3 + 24), (y, y + spot_y))
    i3 = ((x, x + spot_x), (y + spot_y + 12, y + spot_y * 2 + 12))
    i4 = ((x + spot_x + 12, x + spot_x * 2 + 12), (y + spot_y + 12, y + spot_y * 2 + 12))
    i5 = ((x + spot_x * 2 + 24, x + spot_x * 3 + 24), (y + spot_y + 12, y + spot_y * 2 + 12))
    i6 = ((x, x + spot_x), (y + spot_y * 2 + 24, y + spot_y * 3 + 24))
    i7 = ((x + spot_x + 12, x + spot_x * 2 + 12), (y + spot_y * 2 + 24, y + spot_y * 3 + 24))
    i8 = ((x + spot_x * 2 + 24, x + spot_x * 3 + 24), (y + spot_y * 2 + 24, y + spot_y * 3 + 24))
    SPOT = (i0, i1, i2, i3, i4, i5, i6, i7, i8)


def valid_move(x, y):
    if ( (x >= SPOT[0][0][0] and x <= SPOT[0][0][1]) and (y >= SPOT[0][1][0] and y <= SPOT[0][1][1]) and board[0] == ' ' ):
        return 0
    elif ( (x >= SPOT[1][0][0] and x <= SPOT[1][0][1]) and (y >= SPOT[1][1][0] and y <= SPOT[1][1][1]) and board[1] == ' ' ):
        return 1
    elif ( (x >= SPOT[2][0][0] and x <= SPOT[2][0][1]) and (y >= SPOT[2][1][0] and y <= SPOT[2][1][1]) and board[2] == ' ' ):
        return 2
    elif ( (x >= SPOT[3][0][0] and x <= SPOT[3][0][1]) and (y >= SPOT[3][1][0] and y <= SPOT[3][1][1]) and board[3] == ' ' ):
        return 3
    elif ( (x >= SPOT[4][0][0] and x <= SPOT[4][0][1]) and (y >= SPOT[4][1][0] and y <= SPOT[4][1][1]) and board[4] == ' ' ):
        return 4
    elif ( (x >= SPOT[5][0][0] and x <= SPOT[5][0][1]) and (y >= SPOT[5][1][0] and y <= SPOT[5][1][1]) and board[5] == ' ' ):
        return 5
    elif ( (x >= SPOT[6][0][0] and x <= SPOT[6][0][1]) and (y >= SPOT[6][1][0] and y <= SPOT[6][1][1]) and board[6] == ' ' ):
        return 6
    elif ( (x >= SPOT[7][0][0] and x <= SPOT[7][0][1]) and (y >= SPOT[7][1][0] and y <= SPOT[7][1][1]) and board[7] == ' ' ):
        return 7
    elif ( (x >= SPOT[8][0][0] and x <= SPOT[8][0][1]) and (y >= SPOT[8][1][0] and y <= SPOT[8][1][1]) and board[8] == ' ' ):
        return 8
    return None
    

# checking for three(or two) possible way to win for a player
def winner(pl, spot):
    margin = 6

    # row checking
    row_index = spot // 3
    row = board[row_index * 3: row_index * 3 + 3]
    if all(i == pl for i in row):
        pygame.draw.line(surface, RED,
                         (SPOT[row_index * 3][0][0] + margin,
                        round((SPOT[row_index * 3][1][1] - SPOT[row_index * 3][1][0]) / 2) + SPOT[row_index * 3][1][0]),
                        (SPOT[row_index * 3 + 2][0][1] - margin,
                        round((SPOT[row_index * 3][1][1] - SPOT[row_index * 3][1][0]) / 2) + SPOT[row_index * 3][1][0]), 10)
        return True
        
    # column checking
    col_index = spot % 3
    col = [board[col_index + i * 3] for i in range(3)]
    if all(i == pl for i in col):
        pygame.draw.line(surface, RED,
                         (round((SPOT[col_index][0][1] - SPOT[col_index][0][0]) / 2) + SPOT[col_index][0][0],
                        SPOT[col_index][1][0] + margin),
                        (round((SPOT[col_index][0][1] - SPOT[col_index][0][0]) / 2) + SPOT[col_index][0][0],
                        SPOT[col_index + 6][1][1] - margin), 10)
        return True
        
    # diagonally checking
    diag_margin = 20
    if spot % 2 == 0:
        if all(board[i] == pl for i in [0, 4, 8]):
            pygame.draw.line(surface, RED, (SPOT[0][0][0] + diag_margin, SPOT[0][1][0] + diag_margin), (SPOT[8][0][1] - diag_margin, SPOT[8][1][1] - diag_margin), 14)
            return True
        if all(board[i] == pl for i in [2, 4, 6]):
            pygame.draw.line(surface, RED, (SPOT[2][0][1] - diag_margin, SPOT[2][1][0] + diag_margin), (SPOT[6][0][0] + diag_margin, SPOT[6][1][1] - diag_margin), 14)
            return True
        
    return False


# round((end - start) / 2) + start -> find the middle pixel
def make_move(x, y, pl, sp):
    x_margin = 15
    global player

    start_x = SPOT[sp][0][0]
    end_x = SPOT[sp][0][1]
    start_y = SPOT[sp][1][0]
    end_y = SPOT[sp][1][1]

    if (pl == 'X'):
        pygame.draw.line(surface, BLACK, (start_x + x_margin, start_y + x_margin), (end_x - x_margin, end_y - x_margin), 12)
        pygame.draw.line(surface, BLACK, (end_x - x_margin, start_y + x_margin), (start_x + x_margin, end_y - x_margin), 12)
    else:
        pygame.draw.circle(surface, WHITE, (round((end_x - start_x) / 2) + start_x, round((end_y - start_y) / 2) + start_y), 50)
        pygame.draw.circle(surface, BOX_COLOR, (round((end_x - start_x) / 2) + start_x, round((end_y - start_y) / 2) + start_y), 41)
    board[sp] = pl

    # check winner on the go
    if (winner(pl, sp)):
        font = pygame.font.Font(None, 32)
        text_surface = font.render("Player " + pl + " wins!", True, RED)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 32))
        surface.blit(text_surface, text_rect)
        return False
    elif (not (' ' in board)):
        font = pygame.font.Font(None, 32)
        text_surface = font.render("It's a tie!", True, RED)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 32))
        surface.blit(text_surface, text_rect)
        return False
    
    # did make a move, so shifting the player
    player = 'O' if pl == 'X' else 'X'

    return True


# main game loop
running = True
# can u continue playing or not
flag = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            spot = valid_move(mouse_x, mouse_y)

            if (flag):
                flag = make_move(mouse_x, mouse_y, player, spot)
    
    create_board()

    # blitting(copying) surfaces onto the main screen
    screen.blit(surface, (0, 0))

    # update the display
    pygame.display.flip()


# quit game
pygame.quit()
sys.exit()