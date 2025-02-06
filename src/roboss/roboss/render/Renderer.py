import os
import subprocess

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


def draw_board(board):
    # print top row numbers
    print('   ', end='')
    for i in range(len(board[0])):
        print(f' {i % 10} ', end='')
    print()
    # print top outline
    print('  ┌' + '─' * len(board[0]) * 3 + '┐')
    for i, row in enumerate(board):
        # print left outline
        print(i % 10, '│', end='')
        for cell in row:
            match cell:
                case 'X':
                    color = COLORS['magenta']
                case '#':
                    color = COLORS['blue']
                case '^' | '>' | '<' | 'v':
                    color = COLORS['red']
                case _:
                    color = COLORS['white']
            # print cell in color
            print(f" \033[1;{color}m{cell}\033[0m ", end='')
        # print right outline
        print('│')
    # print bottom outline
    print('  └' + '─' * len(board[0]) * 3 + '┘')


def animate_board(frames, id):
    # frames-file
    frames_file = f'frames_{id}.txt'

    # save frames to file
    with open(frames_file, 'w') as f:
        for frame in frames:
            for row in frame:
                f.write(''.join(row) + '\n')
            f.write('\n')

    # run the animation in a new console independent of the current process
    subprocess.Popen(# Run the selected script with the selected input file
        ['cmd', '/k', 'animation.py', os.path.realpath(frames_file)], # Change the working directory for this process
        cwd='C:\\Users\\Frank\\Documents\\2_Programming\\adventofcode\\', # Add the project folder to the python path
        env={**os.environ, 'PYTHONPATH': os.path.abspath(os.path.dirname(__file__))}, # Open a new console window
        creationflags=subprocess.CREATE_NEW_CONSOLE)
