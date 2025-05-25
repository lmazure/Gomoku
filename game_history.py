from typing import Dict
from gomoku import Gomoku

class GameHistory:

    def __init__(self, size:int) -> None:
        self.first_frame = Gomoku(size)
        self.last_frame = self.first_frame.clone()
        self.history = []

    def record_move(self, x: int, y: int) -> Dict:
        result = self.last_frame.manage_move(x, y)
        self.history.append(result['stone_changes'])
        return result

    def get_first_turn(self) -> Gomoku:
        return self.first_frame

    def get_last_turn(self) -> Gomoku:
        return self.last_frame

    def get_nth_turn(self, turn_number: int) -> Gomoku:
        assert turn_number >= 0
        assert turn_number <= len(self.history)
        game = self.first_frame.clone()
        for i in range(0, turn_number):
            for (x,y) in self.history[i]['removed']:
                game.board[x][y] = 0
            for (x,y) in self.history[i]['added']:
                game.board[x][y] = 1 - 2 * (turn_number % 2)
        return game
