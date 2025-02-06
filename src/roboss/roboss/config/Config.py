class Arena:
    PATH = "/bin/arena.json"
    ARENA_KEY = "arena"
    SIZE_KEY = "size"
    SEGMENTS_KEY = "segments"
    OBSTACLE_KEY = "obstacle"


class Flie:
    ID = 0
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
