import copy
from typing import Dict

class Gomoku:

    VALID_MOVE = 0
    INVALID_MOVE = 1
    WIN = 2

    def __init__(self, size: int):
        if (size < 5):
            raise ValueError("Size must be at least 5")
        if ((size % 2) == 0):
            raise ValueError("Size must be odd")
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.turn_number = 0

    def clone(self) -> 'Gomoku':
        # return a clone of the board

        other = self.__class__(self.size)
        other.board = copy.deepcopy(self.board)
        other.turn_number = self.turn_number
        return other

    def set(self, board: list[list[int]], turn_number: int):
        # set the board to a given state
        # board is a 2D array of size 15x15
        # 0 -> empty cell
        # 1 -> black stone
        # -1 -> white stone

        # check board size
        assert len(board) == self.size
        for line in board:
            assert len(line) == self.size

        # check geneneration value
        assert turn_number == self.size * self.size - sum(row.count(0) for row in board)

        # check bumber of stones for each player
        assert 0 <= (sum(row.count(1) for row in board) - sum(row.count(-1) for row in board))  <= 1

        # record data
        self.board = board
        self.turn_number = turn_number

    def manage_move(self, x: int, y: int) -> Dict:
        # manage a move at position (x, y)
        # return a dict (code, message, stone_changes)
        # - code is an (integer) status code
        # - message is a (string) explanation massage
        # - stone_changes is a dict
        #    - added is the list of (int, int) tuples
        #    - removed is the list of (int, int) tuples

        if (x < 0) or (x >= self.size) or (y < 0) or (y >= self.size):
            return  { "status" : self.INVALID_MOVE, "message" : "Move out of the go ban", "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }

        if (self.turn_number == 0):
            if (x != ((self.size-1)/2)) or (y != ((self.size-1)/2)):
                return { "status" : self.INVALID_MOVE, "message" : "First move must be in the center", "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }
        else:
            if (self.board[x][y] != 0):
                return { "status" : self.INVALID_MOVE, "message" : "Move on an already played cell", "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }

        stone_owner = 1 - 2 * (self.turn_number % 2)
        self.board[x][y] = stone_owner
        self.turn_number += 1

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
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (horizontal alignment)", "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }

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
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (vertical alignment)", "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }

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
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (diagonal alignment)", "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }

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
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (anti-diagonal alignment)", "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }

        return { "status" : self.VALID_MOVE, "message" : None, "stone_changes" : { "added" : [ (x, y)], "removed" : [] } }
