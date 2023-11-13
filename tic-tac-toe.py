import pygame
import sys
import math
import random

pygame.init()

# create a 2d screen
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the caption
pygame.display.set_caption("Tic-Tac-Toe")

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED =  (255, 100, 100)
BOX_COLOR = (210, 224, 251)
BG_COLOR = (249, 243, 204)

# define position
SPOT = None
BOTBOX = None

# keep track of the moves
player = 'X'
board = [' ' for i in range(9)]
current_winner = None

# Create separate surfaces for drawing
surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)


def num_empty_squares():
    return board.count(' ')


def empty_squares():
    return ' ' in board


def available_moves():
    return [i for i, x in enumerate(board) if x == ' ']


# for bot, no need to draw lines, just doing the background
def bot_make_move(pl, sp):
    print_line = False
    board[sp] = pl
    if ( winner(pl, sp, print_line) ):
        return pl


def minimax(pl):
    global current_winner
    max_player = player
    other_player = 'O' if pl == 'X' else 'X'

    # first we want to check if the previous move is a winner
    if current_winner == other_player:
        return {'position': None, 'score': 1 * (num_empty_squares() + 1) if other_player == max_player else -1 * (
                        num_empty_squares() + 1)}
    elif not empty_squares():
        return {'position': None, 'score': 0}
    
    if pl == max_player:
        best = {'position': None, 'score': -math.inf}  # each score should maximize
    else:
        best = {'position': None, 'score': math.inf}  # each score should minimize
    for possible_move in available_moves():
        current_winner = bot_make_move(pl, possible_move)
        sim_score = minimax(other_player)  # simulate a game after making that move

        # undo move
        board[possible_move] = ' '
        current_winner = None
        sim_score['position'] = possible_move  # this represents the move optimal next move
         
        if pl == max_player:  # X is max player
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
    return best


def show_state():
    global SPOT

    # background color of the main screen
    screen.fill(BG_COLOR)

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

    win_tie_text()
        
        
def win_tie_text():
    global game_over

    if current_winner:
        font = pygame.font.Font(None, 32)
        text_surface = font.render("Player " + player + " wins!", True, RED)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 32))
        screen.blit(text_surface, text_rect)
        game_over = True
    elif not empty_squares():
        font = pygame.font.Font(None, 32)
        text_surface = font.render("It's a tie!", True, RED)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 32))
        screen.blit(text_surface, text_rect) 
        game_over = True


def legal_move(x, y):
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
def winner(pl, spot, print_line):
    margin = 6

    # row checking
    row_index = spot // 3
    row = board[row_index * 3: row_index * 3 + 3]
    if all(i == pl for i in row):
        if print_line:
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
        if print_line:
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
            if print_line:
                pygame.draw.line(surface, RED, (SPOT[0][0][0] + diag_margin, SPOT[0][1][0] + diag_margin), (SPOT[8][0][1] - diag_margin, SPOT[8][1][1] - diag_margin), 14)
            return True
        if all(board[i] == pl for i in [2, 4, 6]):
            if print_line:
                pygame.draw.line(surface, RED, (SPOT[2][0][1] - diag_margin, SPOT[2][1][0] + diag_margin), (SPOT[6][0][0] + diag_margin, SPOT[6][1][1] - diag_margin), 14)
            return True
        
    return False


# round((end - start) / 2) + start -> find the middle pixel, for player
def make_move(pl, sp):
    global player
    x_margin = 15
    print_line = True

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

    # check winner on a go
    if ( winner(pl, sp, print_line) ):
        return pl
    
    # did make a move, so shifting the player
    player = 'O' if player == 'X' else 'X'
    

def vsbotscope(x, y):
    if ( (x >= BOTBOX[0][0] and x <= BOTBOX[0][1]) and (y >= BOTBOX[1][0] and y <= BOTBOX[1][1]) ):
        return True
    return False


def botplay():
    if num_empty_squares() == 9:
        bot_move = random.choice(available_moves())
    else:
        bot_move = minimax(player)['position']
    return bot_move


# if you already click vsbot button
click = False

# you have decided to play with the bot for the rest of the game
vs_bot = 0

def play(x, y):
    global click, bbappear, current_winner, vs_bot
    spot = legal_move(x, y)

    # for the first turn only
    vsbot = False
    if not click:
        vsbot = vsbotscope(x, y)

    # let the bot goes first
    if vsbot:  
        click = True
        bbappear = False
        # move = botplay()
        # current_winner = make_move(player, move)
        vs_bot = 1

    # player vs player (2 player)
    elif (spot is not None) and (not vs_bot):  
        bbappear = False
        current_winner = make_move(player, spot)
        vs_bot = 0

    # player goes first
    elif vs_bot:
        current_winner = make_move(player, spot)
        move = botplay()
        if move is not None:  #  if the previous move(the player) is not a winner
            current_winner = make_move(player, move)
    

# appear or disappear(bb for botbutton)
bbappear = True

def botbutton():
    global BOTBOX

    pygame.draw.rect(screen, BOX_COLOR, pygame.Rect(screen_width // 2 - 60, 32 - 15, 120, 30))
    
    font = pygame.font.Font(None, 32)
    text_surface = font.render("Versus AI", True, (142, 172, 205))
    text_rect = text_surface.get_rect(center=(screen_width // 2, 32))
    screen.blit(text_surface, text_rect)

    BOTBOX = ((screen_width // 2 - 60, screen_width // 2 - 60 + 120), (32 - 15, 32 - 15 + 30))


# to freeze the game if its over
game_over = False

def freeze():
    if game_over:
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        pygame.event.set_blocked(pygame.KEYDOWN)
        pygame.event.set_blocked(pygame.KEYUP)


# main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            play(mouse_x, mouse_y)


    # print the current state for the game, and also, win or tie.
    show_state()

    if bbappear:
        botbutton()

    # blitting(copying) surfaces onto the main screen
    screen.blit(surface, (0, 0))

    # update the display
    pygame.display.flip()

    freeze()


# quit game
pygame.quit()
sys.exit()
