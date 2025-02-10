"""
Module: Renderer
Provides functionality to render a board, save it to a file, and animate it.

This class is responsible for:
- Rendering a board with ANSI colors.
- Saving board frames to a file.
- Running board animations in a separate process.

Usage:
    - `Renderer.draw_board(board, colors)`: Generates a string representation of the board.
    - `Renderer.draw_boardToFile(board, filename)`: Saves the board representation to a file.
    - `Renderer.animate_board(frames, id)`: Animates a sequence of board frames.
"""

import os
import subprocess
from typing import List, Dict, Optional

from ..config import Config


class Renderer:
    """
    A class for rendering a board, saving frames to a file, and animating the board.

    Attributes:
        default_colors (Dict[str, int]): Default color mapping for board characters.
    """

    default_colors: Dict[str, int] = {"X": Config.Render.Color.MAGENTA, "#": Config.Render.Color.BLUE,
                                     "^": Config.Render.Color.RED, ">": Config.Render.Color.RED,
                                     "<": Config.Render.Color.RED, "v": Config.Render.Color.RED,
                                     "": Config.Render.Color.WHITE  # Default color for unrecognized characters
                                      }

    @classmethod
    def draw_board(cls, board: List[List[str]], colors: Optional[Dict[str, int]] = None) -> Optional[str]:
        """
        Generates a string representation of the board with optional ANSI colors.

        The default colors can be used by setting `colors` to `Renderer.default_colors`.

        Parameters:
            board (List[List[str]]): A 2D list representing the board.
            colors (Optional[Dict[str, int]]): Dictionary mapping characters to color codes.

        Returns:
            Optional[str]: The string representation of the board, or None if the board is empty.
        """
        if not board:
            return None

        board_str = ""

        # Print top row numbers
        board_str += "   "
        for i in range(len(board[0])):
            board_str += f" {i % 10} "
        board_str += "\n"

        # Print top outline
        board_str += "  ┌" + "─" * len(board[0]) * 3 + "┐\n"

        for i, row in enumerate(board):
            # Print left outline
            board_str += f"{i % 10} │"
            for cell in row:
                if colors and cell in colors:
                    # Get color for cell
                    color = colors[cell]
                    # Print cell in color
                    board_str += f" \033[1;{color}m{cell}\033[0m "
                elif colors and "" in colors:
                    # Get default color
                    color = colors[""]
                    # Print cell in color
                    board_str += f" \033[1;{color}m{cell}\033[0m "
                else:
                    # Print cell without color
                    board_str += f" {cell} "
            board_str += "│\n"

        # Print bottom outline
        board_str += "  └" + "─" * len(board[0]) * 3 + "┘\n"

        return board_str

    @classmethod
    def draw_board_to_file(cls, board: List[List[str]], filename: str, colors: Optional[Dict[str, int]] = None,
                           clear: bool = False) -> str:
        """
        Saves the board representation to a file.

        Parameters:
            board (List[List[str]]): A 2D list representing the board.
            filename (str): Name of the file (without extension).
            colors (Optional[Dict[str, int]]): Color mapping dictionary.
            clear (bool): If True, clears the file before writing.

        Returns:
            str: The absolute file path where the board was saved.
        """
        frame = cls.draw_board(board, colors)
        frames_filename = f"frames/{filename}.txt"

        with open(frames_filename, "w" if clear else "a", encoding="utf-8") as f:
            f.write(frame)
            f.write("\n")

        return os.path.realpath(frames_filename)

    @classmethod
    def animate_board(cls, frames: List[List[List[str]]], id: int) -> None:
        """
        Animates a sequence of board frames.

        Parameters:
            frames (List[List[List[str]]]): A list of 2D lists representing board frames.
            id (int): Unique identifier for the animation.

        Returns:
            None
        """
        if not frames:
            return

        frames_filename = f"frames_{id}"
        realpath = ""

        first_frame = True
        for frame in frames:
            realpath = cls.draw_board_to_file(frame, frames_filename, clear=first_frame)
            first_frame = False

        cls.animate_frames(realpath)

    @classmethod
    def animate_frames(cls, frames_file: str) -> None:
        """
        Runs the animation in a new console, independent of the current process.

        Parameters:
            frames_file (str): Path to the file containing the animation frames.

        Returns:
            None
        """
        subprocess.Popen(["cmd", "/k", Config.Render.ANIMATION_FILEPATH, frames_file],
                         env={**os.environ, "PYTHONPATH": os.path.abspath(os.path.dirname(__file__))},
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
