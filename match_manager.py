import os
from gomoku import Gomoku
from random_player import RandomPlayer
from game_history import GameHistory

class MatchManager:
    def __init__(self, size: int):
        self.player1 = RandomPlayer()
        self.player2 = RandomPlayer()
        self.game_history = GameHistory(size)

    def play(self):
        while True:
            board = self.game_history.last_frame.board
            black_takes = self.game_history.last_frame.black_takes
            white_takes = self.game_history.last_frame.white_takes
            if self.game_history.last_frame.turn_number % 2 == 0:
                x, y = self.player2.get_move(board, black_takes, white_takes)
            else:
                white_board = [[-value for value in line] for line in board]
                x, y = self.player1.get_move(white_board, white_takes, black_takes)
            result = self.game_history.record_move(x, y)
            print(result)
            if result["status"] != Gomoku.VALID_MOVE:
                break

    def display_game(self):
        # generate the name of the temporary file
        temp_file_name = "gomoku_replay.html"
        # generate the HTML replay
        self.game_history.generate_html_replay(temp_file_name)
        # open the HTML replay in the default browser
        os.startfile(temp_file_name)

if __name__ == "__main__":
    match_manager = MatchManager(15)
    match_manager.play()
    match_manager.display_game()