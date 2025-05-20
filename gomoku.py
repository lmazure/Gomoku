from typing import Optional


class Gomoku:

    size = 15
    VALID_MOVE = 0
    INVALID_MOVE = 1
    WIN = 2

    def __init__(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.generation = 0

    def set(self, board: list[list[int]], generation: int):
        # set the board to a given state
        # board is a 2D array of size 15x15
        # 0 -> empty cell
        # 1 -> black stone
        # -1 -> white stone

        assert len(board) == self.size
        for line in board:
            assert len(line) == self.size

        self.board = board
        self.generation = generation

    def manage_move(self, x: int, y: int) -> tuple[int, Optional[str]]:
        # manage a move
        # return a tuple (code, message)
        # code is an integer
        # message is a string

        if (x < 0) or (x >= self.size) or (y < 0) or (y >= self.size):
            return self.INVALID_MOVE, "Move out of the go ban"

        if (self.generation == 0):
            if (x != ((self.size-1)/2)) or (y != ((self.size-1)/2)):
                return self.INVALID_MOVE, "First move must be in the center"
        else:
            if (self.board[x][y] != 0):
                return self.INVALID_MOVE, "Move on an already played cell"

        stone_owner = 1 - 2 * (self.generation % 2)
        self.board[x][y] = stone_owner
        self.generation += 1

        x_range_before = 0
        for i in range(-1, -5, -1):
            if (x+i) < 0 :
                break
            if (self.board[x+i][y] == stone_owner):
                x_range_before += 1
            else:
                break
        print(f"x_range_before: {x_range_before}")

        x_range_after = 0
        for i in range(1, 5):
            if (x+i) >= self.size :
                break
            if (self.board[x+i][y] == stone_owner):
                x_range_after += 1
            else:
                break

        if (x_range_before + x_range_after) >= 4:
            return self.WIN, "Player " + str(stone_owner) + " wins (horizontal alignment)"

        y_range_before = 0
        for i in range(-1, -5, -1):
            if (y+i) < 0 :
                break
            if (self.board[x][y+i] == stone_owner):
                y_range_before += 1
            else:
                break

        y_range_after = 0
        for i in range(1, 5):
            if (y+i) >= self.size :
                break
            if (self.board[x][y+i] == stone_owner):
                y_range_after += 1
            else:
                break

        if (y_range_before + y_range_after) >= 4:
            return self.WIN, "Player " + str(stone_owner) + " wins (vertical alignment)"

        xy_range_before = 0
        for i in range(-1, -5, -1):
            print(f"i {i} self.board[{x+i}][{y+i}]= {self.board[x+i][y+i]}")
            if ((x+i) < 0) or ((y+i) < 0):
                break
            if (self.board[x+i][y+i] == stone_owner):
                xy_range_before += 1
            else:
                break
        print(f"xy_range_before: {xy_range_before}")

        xy_range_after = 0
        for i in range(1, 5):
            if ((x+i) >= self.size) or ((y+i) >= self.size):
                break
            if (self.board[x+i][y+i] == stone_owner):
                xy_range_after += 1
            else:
                break
        print(f"xy_range_after: {xy_range_after}")

        if (xy_range_before + xy_range_after) >= 4:
            return self.WIN, "Player " + str(stone_owner) + " wins (diagonal alignment)"

        yx_range_before = 0
        for i in range(-1, -5, -1):
            if ((x+i) < 0) or ((y-i) >= self.size):
                break
            if (self.board[x+i][y-i] == stone_owner):
                yx_range_before += 1
            else:
                break

        yx_range_after = 0
        for i in range(1, 5):
            if ((x+i) >= self.size) or ((y-i) < 0):
                break
            if  (self.board[x+i][y-i] == stone_owner):
                yx_range_after += 1
            else:
                break

        if (yx_range_before + yx_range_after) >= 4:
            return self.WIN, "Player " + str(stone_owner) + " wins (anti-diagonal alignment)"

        return self.VALID_MOVE, None
