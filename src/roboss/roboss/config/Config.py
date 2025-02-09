class Arena:
    PATH = "/home/rosrunner/Documents/Flugrobotik/TeamRoboss/Flugrobotik_WS202425/bin/arena.json"
    ARENA_KEY = "arena"
    SIZE_KEY = "size"
    SEGMENTS_KEY = "segments"
    OBSTACLE_KEY = "obstacle"
    SEGMENT_SIZE = 0.2
    SIZE = 1.45


class Drone:
    A_TOL = 0.3
    WIDTH = 0.115
    # Defines the swaths width, should be the diameter of the Range Finder sensor spread
    OPERATIONAL_WIDTH = WIDTH * 2
    MIN_TURNING_RADIUS = 0.05
    MAX_DIFF_CURV = 0.25
    INITIAL_X = 0.0
    INITIAL_Y = 0.0


class Flie:
    ID = 1
    SAFEFLIE_NAME = f"safeflie{ID}"
    TF_NAME = f"cf{ID}"
    NODE_NAME = "tha_flie"
    BASE_FRAME = "world"
    QOS_PROFILE = 10


class Field:
    TARGET = "target"
    TRANSLATION = "translation"
    ZRANGE = "zrange"


class Topic:
    TAKEOFF = Flie.SAFEFLIE_NAME + "/takeoff"
    LAND = Flie.SAFEFLIE_NAME + "/land"
    SEND_TARGET = Flie.SAFEFLIE_NAME + "/send_target"
    EXAMPLE_ROUTE = Flie.SAFEFLIE_NAME + "/example_route"


class Render:
    OBSTACLE = "#"
    EMPTY = " "

    class Color:
        BLACK = 30
        RED = 31
        GREEN = 32
        YELLOW = 33
        BLUE = 34
        MAGENTA = 35
        CYAN = 36
        GREY = 37
        WHITE = 38
