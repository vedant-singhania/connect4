import io
import numpy as np
import subprocess
import sys
import json
import random
import time

ROW_COUNT = 6  # height
COLUMN_COUNT = 7  # width

stderr1_txt = open("stderr1.txt", "w")
stderr2_txt = open("stderr2.txt", "w")

# Create Subprocesses
PLAYER_1 = subprocess.Popen(
    "python3 player_naive.py",
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=stderr1_txt
)
#
# PLAYER_1 = subprocess.Popen(
#     "/Applications/Racket\ v7.2/bin/racket connect-four-naive.rkt",
#     shell=True,
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=stderr1_txt
# )

#
# PLAYER_2 = subprocess.Popen(
#     "python3 player_naive.py",
#     shell=True,
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=stderr2_txt
# )

# PLAYER_2 = subprocess.Popen(
#     "/Applications/Racket\ v7.2/bin/racket connect-four-naive.rkt",
#     shell=True,
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=stderr2_txt
# )

# PLAYER_2 = subprocess.Popen(
#     "./player.mac",
#     shell=True,
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=stderr2_txt
# )

PLAYER_2 = subprocess.Popen(
    "python3 connect-four-naive.py --player 2 --width 6 --height 7",
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=stderr2_txt
)

#
# PLAYER_2 = subprocess.Popen(
#     "python3 player_moin.py",
#     shell=True,
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=stderr2_txt
# )


# Define standard ports for stdin, stdout and stderr communication
stdin1 = io.TextIOWrapper(
    PLAYER_1.stdin,
    encoding='utf-8',
    line_buffering=True,  # send data on newline
)

stdin2 = io.TextIOWrapper(
    PLAYER_2.stdin,
    encoding='utf-8',
    line_buffering=True,  # send data on newline
)


stdout1 = io.TextIOWrapper(
    PLAYER_1.stdout,
    encoding='utf-8',
)

stdout2 = io.TextIOWrapper(
    PLAYER_2.stdout,
    encoding='utf-8',
)

# initialize board state
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    board = board.astype(int)
    return board


def board_to_json(board):
    array_to_list = board.tolist()
    return json.dumps({'grid': array_to_list})



# def json_to_board():

# play move by player
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# checks to see if column chosen is full
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def play_move(board, col, player_move):
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, player_move)  # new board state
        print_board(board)
        # check to see if board in winning state
        if winning_move(board, player_move):
            print("Player "+str(player_move)+" has won!")
            return True  # game_over
        else:
            return False  # game_over=false
    else:  # invalid location
        print("Invalid Location!")

def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # check horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # check right diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # check left diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True



# start a new game
def start_new_game():
    print("***Starting New Game***")

    game_board = create_board()  # start new board
    print_board(game_board)
    game_over = False
    turn = 0  # 0 for player1, 1 for player2
    number_of_moves = 0

    # start game loop
    while not game_over:
        # convert board to json
        game_board_json = board_to_json(game_board) + '\n'
        game_board_json = game_board_json
        print("Sending JSON to player" + str(turn+1) + ": -->")


        # alternate turns between players
        if turn == 0:
            stderr1_txt.write(game_board_json)
            stdin1.write(game_board_json)  # send board state via stdin
            time.sleep(0.02)
            print(game_board_json)
            print("Player 1:")
            result = stdout1.readline()  # json with "move" key
            try:
                x = json.loads(result.rstrip())  # strip endline
            except ValueError as e:
                # print(e)
                print(result)
                stderr1_txt.write(result)
                stdout1.flush()
                break
            stderr1_txt.write(result)
            game_col = x['move']  # player column choice
            print(result.rstrip())
            player_number = 1

        else:
            stderr2_txt.write(game_board_json)
            stdin2.write(game_board_json)  # send board state via stdin
            time.sleep(0.03)
            print(game_board_json)
            print("Player 2:")
            result = stdout2.readline()  # json with "move" key
            try:
                x = json.loads(result.rstrip())  # strip endline
            except ValueError as e:
                print(e)
                stderr2_txt.write(result)
                print(result)
                stdout2.flush()
                break
            stderr2_txt.write(result)
            game_col = x['move']  # player column choice
            print(result.rstrip())
            player_number = 2

        #game_col = random.randrange(0, 7)
        game_over = play_move(game_board, game_col, player_number)  # play move and check if game over
        turn = (turn + 1) % 2  # alternate turn between players (0,1)
        time.sleep(0.02)
        number_of_moves += 1  # count total number of moves in the game
    else:
        print('# of moves: ' + str(number_of_moves))
        print('---GAME OVER---')


def main():
    game_type = int(input("Enter 1 for Single Game\nEnter 2 for Head-to-Head Play: "))

    if game_type == 1:
        start_new_game()
    if game_type == 2:
        i = 0
        while i != 5:
            start_new_game()
            i += 1


# invoke main function
if __name__ == "__main__":
    main()




