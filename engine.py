## Main Tic Tac Toe Engine
Board_width = 3
Board_height = 3
import random
from collections import Counter
# Step 1 is to create a new tic tac toe board
def new_board() -> list:
    return [[None for n in range(Board_width)] for m in range(Board_height)]

# Step 2 is to create a render function so humans can view the board
def render(board) -> None:
    
    rows = []
    for y in range(0,Board_height):
        row = []
        for x in range(0, Board_width):
            row.append(board[x][y])
        rows.append(row)
    
    print('  0 1 2')
    print('  -----')
    row_num = 0
    for row in rows:
        output_row = ''
        for space in row:
            if space is None:
                output_row += ' '
            else:
                output_row += space
        print("%d|%s|" % (row_num, ' '.join(output_row)))
        row_num += 1
    pass

# Step 3 is to create a function that returns coordinates of the players' chose move as a 2 element tuple
def get_move() -> tuple[int, int]:
    while True:
        try:
            x_coord = int(input('What is your move\'s X coordinate? ' ))
            y_coord = int(input('What is your move\'s Y coordinate? ' ))
            if  0 <= x_coord < 3 and 0 <= y_coord < 3:
                break
            else:
                print("Number out of range. Please enter a number between 0 and 2 (inclusive) and try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    return (x_coord, y_coord)

# Step 4 is to create a function that takes in coordinates and makes a move for the given player
def make_move(board,move_coords,player) -> list:
    acceptable_players = ['X', 'O']
    if player.upper() not in acceptable_players:
       raise Exception('Player must be either X or O')
    
    x = move_coords[0]
    y = move_coords[1]
    new_board = board
    if board[x][y] is not None:
        raise Exception('Can\'t make move ' + str(move_coords) +', square already taken!')
    new_board[x][y] = player.upper()
    return new_board

# Step 5 is to check if the board is full
def board_isnt_full(board) -> bool:
    for line in board:
        for square in line:
            if square is None:
                return True
    else:
        return False

# Step 6 is to create a function that alternates the players for each turn
def switch_player(player) -> str:
    if player == 'X':
        return 'O'
    elif player == 'O':
        return 'X'

# Step 7 is to determine if there is a winner given the current board, also returns all combos of possible winning lists
def get_winner(board) -> str:
    rows = []
    for line in board:
        rows.append(line)
    cols = []
    for i in range(0,3):
        col = []
        for k in range(0,3):
            col.append(board[i][k])
        cols.append(col)
    diags = []
    diag_down = []
    diag_up = []
    for i in range(0,3):
        diag_down.append(board[i][i])
        diag_up.append(board[i][2-i])
    diags.append(diag_down)
    diags.append(diag_up)
    all_combos = []
    for i in range(0,3):
        all_combos.append(rows[i])
        all_combos.append(cols[i])
    all_combos.append(diags[0])
    all_combos.append(diags[1])
    for entries in all_combos:
        if all(x == entries[0] for x in entries) == True:
            return entries[0]
    return None

# Step 8 is to create a play function that combines the above into a tic tac toe game 
def play(player1,player2):
    board = new_board()
    player = str(input('Which player is going first? Enter X or O: ' )).upper()
    render(board)
    count = 0
    while board_isnt_full(board):
        if count % 2 == 0:
            player_name = player1
        else:
            player_name = player2
        
        count += 1

        if player_name == "human_player":
            move_coords = human_player(board, player)
        elif player_name == "random_ai":
            move_coords = random_ai(board,player)
        elif player_name == "finds_winning_moves_ai":
            move_coords = finds_winning_moves_ai(board,player)[0]
        elif player_name == "finds_winning_and_losing_ai":
            move_coords = finds_winning_and_losing_ai(board,player)
        # move_coords  = get_move() # use if playing as a human
        # move_coords = finds_winning_and_losing_ai(board, player)
        # move_coords = human_player(board, player)
        board = make_move(board, move_coords, player)
        render(board)
        winner = get_winner(board)
        if winner is not None:
            print(winner + ' is the winner!')
            break
        player = switch_player(player)
    if board_isnt_full(board) is False and winner is None:
        print('Tie! There is no winner.')


# Part 2
# Step 1 is to create an ai that returns a random, legal move
def random_ai(board, player) -> tuple[int, int]:
    while True:
        x_coord = random.randint(0,2)
        y_coord = random.randint(0,2)
        if board[x_coord][y_coord] is None:
            break
    return (x_coord,y_coord)

# Step 2 is to create an ai that returns a winning move or random if no winning move
def finds_winning_moves_ai(board, player) -> tuple[tuple[int, int], bool]:
    all_lines_coords = get_all_lines_coords()
    for line in all_lines_coords:
        n_me = 0
        n_opp = 0
        n_empty = 0
        coord = None
        winning_move = False
        for (x,y) in line:
            val = board[x][y]
            if val == player:
                n_me += 1
            elif val is None:
                n_empty += 1
                coord = (x,y)
            else:
                n_opp += 1
        if n_me == 2 and n_empty == 1:
            winning_move = True
            return coord, winning_move
        
    if winning_move is False:
        return [random_ai(board,player), winning_move]

def get_all_lines_coords() -> tuple[int,int]:
    rows = []
    for y in range(0,Board_height):
        row = []
        for x in range(0,Board_width):
            row.append((x,y))
        rows.append(row)

    cols = []
    for x in range(0,Board_width):
        col = []
        for y in range(0,Board_height):
            col.append((x,y))
        cols.append(col)
    
    diagonals = [
        [(0,0),(1,1),(2,2)], 
        [(0,2),(1,1),(2,0)]
    ]
    return rows + cols + diagonals

def finds_winning_and_losing_ai(board,player) -> tuple[int,int]:
    """call find winning moves ai function. If this player
    has a winning move, return it.
    if not, call winning moves ai function for the other player.
    If they have a winning move, return it so the other player can block.
    If neither has a winning move, random_ai."""
    if finds_winning_moves_ai(board, player)[1] is True:
        return finds_winning_moves_ai(board, player)[0]
    else:
        player = switch_player(player)
        if finds_winning_moves_ai(board, player)[1] is True:
            return finds_winning_moves_ai(board, player)[0]
        else:
            player = switch_player(player)
            return random_ai(board,player)

def human_player(board, player) -> tuple[int,int]:
    return get_move()

play('finds_winning_and_losing_ai','random_ai')
