import json
from typing import Dict
import os
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

    def generate_html_replay(self, html_filepath: str, template_filename: str = "gomoku_replay_template.html"):
        """
        Generates an HTML file displaying the game replay.

        Args:
            html_filepath (str): The path to save the generated HTML file.
            template_filename (str): The name of the HTML template file.
                                     Assumed to be in the same directory as this script,
                                     or a path relative to it.
        Returns:
            bool: True if successful, False otherwise.
        """
        turn_data_list = []

        # Turn 0: Initial state
        initial_game_state = self.get_nth_turn(0)
        turn_data_list.append({
            "turn_number": 0,
            "board": initial_game_state.board,
            "black_captures": initial_game_state.black_takes,
            "white_captures": initial_game_state.white_takes,
            "current_player": 1, # Black to move first
            "last_move": None
        })

        for i in range(len(self.history)):
            turn_number = i + 1
            game_state_at_turn = self.get_nth_turn(turn_number)
            move_info = self.history[i] # (x, y, removed_stones)
            
            # Player who will make the *next* move after this state is displayed
            next_player = -1 if (i % 2 == 0) else 1 # If black just moved (i is even), next is white. Else black.

            turn_data_list.append({
                "turn_number": turn_number,
                "board": game_state_at_turn.board,
                "black_captures": game_state_at_turn.black_takes,
                "white_captures": game_state_at_turn.white_takes,
                "current_player": next_player,
                "last_move": [move_info[0], move_info[1]] # Only x, y of the move
            })

        full_game_data = {
            "board_size": self.first_frame.size,
            "total_turns": len(self.history),
            "all_moves": self.history, 
            "turn_data": turn_data_list
        }

        if not os.path.isabs(template_filename):
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                template_path = os.path.join(script_dir, template_filename)
            except NameError: # __file__ is not defined (e.g. in REPL, or if code is exec'd)
                # Fallback: try current working directory, or require absolute path for template
                print("Warning: Could not determine script directory. Assuming template is in CWD or an absolute path is given.")
                template_path = template_filename 
        else:
            template_path = template_filename
            
        try:
            with open(template_path, 'r', encoding='utf-8') as f_template:
                template_content = f_template.read()
        except FileNotFoundError:
            print(f"Error: HTML template file '{template_path}' not found.")
            return False 
        except Exception as e:
            print(f"Error reading template file '{template_path}': {e}")
            return False

        game_data_json = json.dumps(full_game_data, indent=None) 
        html_content = template_content.replace("__GAME_DATA_PLACEHOLDER__", game_data_json, 1)

        try:
            with open(html_filepath, 'w', encoding='utf-8') as f_output:
                f_output.write(html_content)
            print(f"HTML replay successfully generated at: {html_filepath}")
            return True
        except Exception as e:
            print(f"Error writing HTML file '{html_filepath}': {e}")
            return False
