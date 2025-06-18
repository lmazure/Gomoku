import json
from typing import Dict
from gomoku import Gomoku

class GameHistory:

    def __init__(self, size: int) -> None:
        """
        Initializes a GameHistory instance.

        Args:
            size (int): The size of the Gomoku board.

        Attributes:
            first_frame (Gomoku): The initial state of the Gomoku game.
            last_frame (Gomoku): The current state of the Gomoku game.
            history (list): The history of moves made in the game.
        """
        self.first_frame = Gomoku(size)
        self.last_frame = self.first_frame.clone()
        self.history = []

    def record_move(self, x: int, y: int) -> Dict:
        """
        Records a move in the game history.

        Args:
            x (int): The x-coordinate of the move.
            y (int): The y-coordinate of the move.

        Returns:
            Dict: The result of the move.
        """
        result = self.last_frame.manage_move(x, y)
        self.history.append((x, y, result['removed_stones']))
        return result

    def get_first_turn(self) -> Gomoku:
        """
        Returns the first turn of the game.

        Returns:
            Gomoku: The initial state of the Gomoku game.
        """
        return self.first_frame

    def get_last_turn(self) -> Gomoku:
        """
        Returns the last turn of the game.

        Returns:
            Gomoku: The current state of the Gomoku game.
        """
        return self.last_frame

    def get_nth_turn(self, turn_number: int) -> Gomoku:
        """
        Returns the turn at the given index.

        Args:
            turn_number (int): The index of the turn to return.

        Returns:
            Gomoku: The state of the Gomoku game at the given turn.
        """
        assert turn_number >= 0
        assert turn_number <= len(self.history)
        game = self.first_frame.clone()
        for i in range(0, turn_number):
            x, y, removed_stones = self.history[i]
            if (i % 2):
                game.board[x][y] = -1
                game.white_takes += len(removed_stones) // 2
            else:
                game.board[x][y] = 1
                game.black_takes += len(removed_stones) // 2
            for (xr, yr) in removed_stones:
                game.board[xr][yr] = 0
        return game

    def save_to_file(self, filepath: str):
        """
        Saves the game history to a file in JSON format.

        Args:
            filepath (str): The path to the file to save the game history to.
        """
        data = {
            'size': self.first_frame.size,
            'history': self.history
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'GameHistory':
        """
        Loads a game history from a file.

        Args:
            filepath (str): The path to the file to load the game history from.

        Returns:
            GameHistory: The loaded game history.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        size = data['size']
        history_moves = data['history']
        
        game_history = cls(size)
        for move in history_moves:
            x, y, _ = move
            game_history.record_move(x, y)
            
        return game_history
