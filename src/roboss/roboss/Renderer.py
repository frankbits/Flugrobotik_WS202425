# for i in range(0, 100):
#     print(f" \033[1;{i}m{i}\033[0m ", end='')
import os
import subprocess

class Renderer:
    COLORS = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'grey': 37,
        'white': 38
    }

    defaultColors = {
        'X': COLORS['magenta'],
        '#': COLORS['blue'],
        '^': COLORS['red'],
        '>': COLORS['red'],
        '<': COLORS['red'],
        'v': COLORS['red'],
        '': COLORS['white'] # default color
    }

    @classmethod
    def drawBoard(cls, board: list[list[str]], colors: dict = None):
        """
        Draw the board and return it as a string

        The default colors can be used by setting the colors attribute to ``Renderer.defaultColors``.

        :param board: Array describing the board
        :param colors: Dictionary with colors per character
        :return: String representation of the board
        """
        if not board:
            return
        
        board_str = ''
        
        # print top row numbers
        board_str += '   '
        for i in range(len(board[0])):
            board_str += f' {i%10} '
        board_str += '\n'
        # print top outline
        board_str += '  ┌' + '─' * len(board[0]) * 3 + '┐\n'
        for i, row in enumerate(board):
            # print left outline
            board_str += f'{i%10} │'
            for cell in row:
                if colors and cell in colors:
                    # get color for cell
                    color = colors[cell]
                    # print cell in color
                    board_str += f" \033[1;{color}m{cell}\033[0m "
                elif colors and '' in colors:
                    # get default color
                    color = colors['']
                    # print cell in color
                    board_str += f" \033[1;{color}m{cell}\033[0m "
                else:
                    # print cell without color
                    board_str += f' {cell} '
            # print right outline
            board_str += '│\n'
        # print bottom outline
        board_str += '  └' + '─' * len(board[0]) * 3 + '┘\n'

        return board_str

    @classmethod
    def drawBoardToFile(cls, board, filename, colors=None, clear=False):
        """
        Draw the board to a file
        :param board: Array describing the board
        :param filename: Filename for the file without extension
        :param colors: Dictionary with colors per character (e.g. ``Renderer.defaultColors``)
        :param clear: Clear the file before writing
        :return: Real path to the file
        """
        frame = cls.drawBoard(board, colors)

        # frames-file
        frames_filename = f'{filename}.txt'

        # save frames to file
        with open(frames_filename, 'w' if clear else 'a', encoding="utf-8") as f:
            f.write(frame)
            f.write('\n')

        return os.path.realpath(frames_filename)

    @classmethod
    def animateBoard(cls, frames, id):
        if not frames:
            return

        # frames-file
        frames_filename = f'frames_{id}'

        # save frames to file
        realpath = ''
        first_frame = True
        for frame in frames:
            realpath = cls.drawBoardToFile(frame, frames_filename, clear=first_frame)
            first_frame = False

        cls.animate_frames(realpath)

    @classmethod
    def animate_frames(cls, frames_file: str):
        """
        Run the animation in a new console independent of the current process
        :param frames_file: Path to the file containing the frames
        :return: None
        """
        subprocess.Popen(
            # Run the selected script with the selected input file
            ['cmd', '/k', 'animation.py', frames_file],
            # Add the project folder to the python path
            env={**os.environ, 'PYTHONPATH': os.path.abspath(os.path.dirname(__file__))},
            # Open a new console window
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )