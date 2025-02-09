# from os import system
import sys
import time

# get first parameter from command line
if len(sys.argv) > 1:
    inputFile = sys.argv[1]
else:
    exit("No input file given")

# get frames from file
frames = []
with open(inputFile, 'r', encoding="utf-8") as f:
    frame = ''
    for line in f:
        if line == '\n':
            frames.append(frame)
            frame = ''
        else:
            frame += line
    frames.append(frame)

# move cursor to top left
# print(f"\033[0;0H", end="")

# move cursor to bottom right
# print(f"\033[{len(frames[0]) + 3};{len(frames[0][0]) * 3 + 3}H", end="")

# move cursor up
# print(f"\033[{nlines}A", end="")

# save current cursor position
print("\033[s", end="")

# restore cursor position
# print("\033[u", end="")

# clear screen
# system('clear') # linux
# system('cls') # windows
# print("\033[2J", end="")

# hide cursor
print("\033[?25l", end="")

# show cursor again after KeyboardInterrupt
try:
    while True:
        nlines = len(frames[0])
        for frame in frames:
            # restore cursor position
            print("\033[u", end="")
            print(frame)
            time.sleep(.1)
except KeyboardInterrupt:
    # show cursor
    print("\033[?25h", end="")
