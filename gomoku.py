import copy
from typing import Dict

class Gomoku:

    VALID_MOVE = 0
    INVALID_MOVE = 1
    WIN = 2

    def __init__(self, size: int):
        """
        Initializes a Gomoku game board.

        Args:
            size (int): The size of the board. Must be an odd integer greater than or equal to 5.

        Raises:
            ValueError: If the size is less than 5 or not an odd integer.

        Attributes:
            board (list[list[int]]): A 2D list representing the board state.
                - 0 -> empty cell
                - 1 -> black stone
                - -1 -> white stone
            size (int): The size of the board.
            turn_number (int): The current turn number.
            black_takes (int): The number of black stone pairs taken.
            white_takes (int): The number of white stone pairs taken.
        """
        if (size < 5):
            raise ValueError("Size must be at least 5")
        if ((size % 2) == 0):
            raise ValueError("Size must be odd")
        self.board:list[list[int]] = [[0 for _ in range(size)] for _ in range(size)]
        self.size:int = size
        self.turn_number:int = 0
        self.black_takes:int = 0
        self.white_takes:int = 0

    def clone(self) -> 'Gomoku':
        """
        Returns a clone of the board.

        Returns:
            Gomoku: A clone of the board.
        """

        other = self.__class__(self.size)
        other.board = copy.deepcopy(self.board)
        other.turn_number = self.turn_number
        other.black_takes = self.black_takes
        other.white_takes = self.white_takes
        return other

    def set(self, board: list[list[int]], black_takes: int, white_takes: int, turn_number: int):
        """
        Sets the board to a given state.

        Args:
            board (list[list[int]]): The board to set.
                - 0 -> empty cell
                - 1 -> black stone
                - -1 -> white stone
            black_takes (int): The number of black stone pairs taken.
            white_takes (int): The number of white stone pairs taken.
            turn_number (int): The turn number.
        """

        # check board size
        assert len(board) == self.size
        for line in board:
            assert len(line) == self.size

        # check number of stones for each player
        assert ((turn_number + 1) // 2) == sum(row.count(1) for row in board) + 2 * white_takes
        assert (turn_number // 2) == sum(row.count(-1) for row in board) + 2 * black_takes

        # record data
        self.board = board
        self.turn_number = turn_number
        self.black_takes = black_takes
        self.white_takes = white_takes

    def manage_move(self, x: int, y: int) -> Dict:
        """
        Manages a move at position (x, y).

        Args:
            x (int): The x-coordinate of the move.
            y (int): The y-coordinate of the move.

        Returns:
            Dict: The result of the move
            - code is an (integer) status code
                - VALID_MOVE = 0
                - INVALID_MOVE = 1
                - WIN = 2
            - message is a (string) explanation message
            - removed_stones is a list of (int, int) tuples
        """

        removed_stones = []

        if (x < 0) or (x >= self.size) or (y < 0) or (y >= self.size):
            return  { "status" : self.INVALID_MOVE, "message" : "Move out of the go ban", "removed_stones" : removed_stones }

        if (self.turn_number == 0):
            if (x != ((self.size-1)/2)) or (y != ((self.size-1)/2)):
                return { "status" : self.INVALID_MOVE, "message" : "First move must be in the center", "removed_stones" : removed_stones }
        elif (self.turn_number == 2):
            if (x >= ((self.size-5)/2)) and (y >= ((self.size-5)/2)) and (x < ((self.size+5)/2)) and (y < ((self.size+5)/2)):
                return { "status" : self.INVALID_MOVE, "message" : "Third move must be out of central 5×5 square", "removed_stones" : removed_stones }
        else:
            if (self.board[x][y] != 0):
                return { "status" : self.INVALID_MOVE, "message" : "Move on an already played cell", "removed_stones" : removed_stones }

        stone_owner = 1 - 2 * (self.turn_number % 2)
        self.board[x][y] = stone_owner
        self.turn_number += 1

        if (x >= 3):
            if (self.board[x-3][y] == stone_owner) and (self.board[x-2][y] == -stone_owner) and (self.board[x-1][y] == -stone_owner):
                removed_stones.append((x-2, y))
                removed_stones.append((x-1, y))
                self.board[x-2][y] = 0
                self.board[x-1][y] = 0

        if (x >= 3) and (y >= 3):
            if (self.board[x-3][y-3] == stone_owner) and (self.board[x-2][y-2] == -stone_owner) and (self.board[x-1][y-1] == -stone_owner):
                removed_stones.append((x-2, y-2))
                removed_stones.append((x-1, y-1))
                self.board[x-2][y-2] = 0
                self.board[x-1][y-1] = 0

        if (y >= 3):
            if (self.board[x][y-3] == stone_owner) and (self.board[x][y-2] == -stone_owner) and (self.board[x][y-1] == -stone_owner):
                removed_stones.append((x, y-2))
                removed_stones.append((x, y-1))
                self.board[x][y-2] = 0
                self.board[x][y-1] = 0

        if (x < self.size-3) and (y >= 3):
            if (self.board[x+3][y-3] == stone_owner) and (self.board[x+2][y-2] == -stone_owner) and (self.board[x+1][y-1] == -stone_owner):
                removed_stones.append((x+2, y-2))
                removed_stones.append((x+1, y-1))
                self.board[x+2][y-2] = 0
                self.board[x+1][y-1] = 0

        if (x < self.size-3):
            if (self.board[x+3][y] == stone_owner) and (self.board[x+2][y] == -stone_owner) and (self.board[x+1][y] == -stone_owner):
                removed_stones.append((x+2, y))
                removed_stones.append((x+1, y))
                self.board[x+2][y] = 0
                self.board[x+1][y] = 0

        if (x < self.size-3) and (y < self.size-3):
            if (self.board[x+3][y+3] == stone_owner) and (self.board[x+2][y+2] == -stone_owner) and (self.board[x+1][y+1] == -stone_owner):
                removed_stones.append((x+2, y+2))
                removed_stones.append((x+1, y+1))
                self.board[x+2][y+2] = 0
                self.board[x+1][y+1] = 0

        if (y < self.size-3):
            if (self.board[x][y+3] == stone_owner) and (self.board[x][y+2] == -stone_owner) and (self.board[x][y+1] == -stone_owner):
                removed_stones.append((x, y+2))
                removed_stones.append((x, y+1))
                self.board[x][y+2] = 0
                self.board[x][y+1] = 0

        if (x >= 3) and (y < self.size-3):
            if (self.board[x-3][y+3] == stone_owner) and (self.board[x-2][y+2] == -stone_owner) and (self.board[x-1][y+1] == -stone_owner):
                removed_stones.append((x-2, y+2))
                removed_stones.append((x-1, y+1))
                self.board[x-2][y+2] = 0
                self.board[x-1][y+1] = 0

        if (stone_owner == 1):
            self.black_takes += len(removed_stones) // 2
            if (self.black_takes >= 5):
                return { "status" : self.WIN, "message" : "Player 1 wins (5 takes)", "removed_stones" : removed_stones }
        else:
            self.white_takes += len(removed_stones) // 2
            if (self.white_takes >= 5):
                return { "status" : self.WIN, "message" : "Player 2 wins (5 takes)", "removed_stones" : removed_stones }

        x_range_before = 0
        for i in range(-1, -5, -1):
            if (x+i) < 0 :
                break
            if (self.board[x+i][y] == stone_owner):
                x_range_before += 1
            else:
                break

        x_range_after = 0
        for i in range(1, 5):
            if (x+i) >= self.size :
                break
            if (self.board[x+i][y] == stone_owner):
                x_range_after += 1
            else:
                break

        if (x_range_before + x_range_after) >= 4:
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (horizontal alignment)", "removed_stones" : removed_stones }

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
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (vertical alignment)", "removed_stones" : removed_stones }

        xy_range_before = 0
        for i in range(-1, -5, -1):
            if ((x+i) < 0) or ((y+i) < 0):
                break
            if (self.board[x+i][y+i] == stone_owner):
                xy_range_before += 1
            else:
                break

        xy_range_after = 0
        for i in range(1, 5):
            if ((x+i) >= self.size) or ((y+i) >= self.size):
                break
            if (self.board[x+i][y+i] == stone_owner):
                xy_range_after += 1
            else:
                break

        if (xy_range_before + xy_range_after) >= 4:
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (diagonal alignment)", "removed_stones" : removed_stones }

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
            return { "status" : self.WIN, "message" : "Player " + str(stone_owner) + " wins (anti-diagonal alignment)", "removed_stones" : removed_stones }

        return { "status" : self.VALID_MOVE, "message" : None, "removed_stones" : removed_stones }
