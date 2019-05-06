import sys
import random
import numpy as np
from numpy import array
import json
import time
import ast


def is_valid_location(board, col):
    return board[6-1][col] == 0


def play():
    while True:
        next_line = sys.stdin.readline()  # receive json stdin
        sys.stderr.flush()  # flush stderr
        if not next_line:
            break
        json_input = json.loads(next_line.rstrip())  # receive json
        game_board_list = json_input['grid']  # game board as list
        game_board = array(game_board_list)  # game board as np.array

        random_number = random.randrange(0, 7)
        while not is_valid_location(game_board, random_number):  # check if choice is valid, if not choose again
            random_number = random.randrange(0, 7)

        json_data = '{"move":'+str(random_number)+'}\n'  # construct json with move selection stdout
        python_obj = json.loads(json_data)
        # time.sleep(1)
        sys.stdout.write(json.dumps(python_obj) + '\n')  # write to stdout
        sys.stdout.flush()  # flush stdout

def main():
    play()

    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()

# invoke main function
if __name__ == "__main__":
    main()
