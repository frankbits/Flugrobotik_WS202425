"""
Module: ASCII Animation Player
Reads frames from a text file and animates them in the terminal.

This script reads ASCII animation frames from a file and continuously plays them in the terminal.
It uses ANSI escape codes to manipulate cursor positioning, hide the cursor, and restore it after
a keyboard interrupt.

Usage:
    python script.py <input_file>

Where:
    <input_file> is a text file where frames are separated by blank lines.

Features:
    - Reads ASCII frames from a text file.
    - Uses ANSI escape codes to control cursor position and visibility.
    - Continuously loops through the frames until interrupted (Ctrl+C).
"""

import sys
import time

# Ensure an input file is provided
if len(sys.argv) > 1:
    input_file: str = sys.argv[1]
else:
    exit("Error: No input file provided.")

# Read frames from the file
frames: list[str] = []
with open(input_file, 'r', encoding="utf-8") as f:
    frame: str = ''
    for line in f:
        if line == '\n':  # Empty line indicates a new frame
            frames.append(frame)
            frame = ''
        else:
            frame += line
    frames.append(frame)  # Append the last frame

# Save the current cursor position
print("\033[s", end="")

# Hide the cursor to avoid flickering
print("\033[?25l", end="")

try:
    while True:
        for frame in frames:
            # Restore cursor position to overwrite the previous frame
            print("\033[u", end="")
            print(frame, end="", flush=True)
            time.sleep(0.1)  # Delay between frames
except KeyboardInterrupt:
    # Show cursor again when interrupted
    print("\033[?25h", end="")
