def convert_string_to_board(board: str) -> list[list[int]]:
    # convert the go ban display to a list of strings
    # '.' -> 0
    # '●' -> 1
    # '○' -> -1
    tempo = [[int(cell == '●') - int(cell == '○') for cell in line] for line in board.splitlines()]
    return [list(i) for i in zip(*tempo)]

def convert_board_to_string(board: list[list[int]]) -> str:
    # convert the list of strings to a go ban display
    # 0 -> '.'
    # 1 -> '●'
    # -1 -> '○'
    str = ["" for _ in board]
    for line in board:
        for i, cell in enumerate(line):
            str[i] += ('.' if cell == 0 else '●' if cell == 1 else '○')
    return '\n'.join(str)
