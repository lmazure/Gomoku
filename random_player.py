import random
from typing import Tuple

class RandomPlayer:
    def __init__(self):
        pass

    def get_move(self, board: list[list[int]], black_takes: int, white_takes: int) -> Tuple[int, int]:
        board_size = len(board)
        turn_number = black_takes + white_takes + (board_size* board_size - sum(row.count(0) for row in board))
        if turn_number == 0:
            return board_size // 2, board_size // 2
        while True:
            x = random.randint(0, board_size-1)
            y = random.randint(0, board_size-1)
            if board[x][y] == 0:
                if (turn_number == 2) and \
                  (x >= ((board_size-5)/2)) and (y >= ((board_size-5)/2)) and \
                  (x < ((board_size+5)/2)) and (y < ((board_size+5)/2)):
                    continue
                return x, y
