"""
Module: Config
Configuration module for drone, arena, and rendering settings.

This module defines various configuration constants used across the application,
including the arena dimensions and file path, drone operational parameters, unique
identifiers and topics for the drone (Flie), field key names, communication topics,
and rendering characters and colors.
"""


class Arena:
    """
    Configuration for the arena.

    Attributes:
        PATH (str): Path to the arena JSON file.
        ARENA_KEY (str): Key used in the JSON to identify the arena.
        SIZE_KEY (str): Key used in the JSON to denote the arena size.
        SEGMENTS_KEY (str): Key used in the JSON for the arena segments.
        OBSTACLE_KEY (str): Key used in the JSON to mark an obstacle.
        SEGMENT_SIZE (float): The size (in meters) of each segment.
        SIZE (float): The overall arena size (in meters).
    """
    PATH: str = "/home/rosrunner/Documents/Flugrobotik/TeamRoboss/Flugrobotik_WS202425/bin/arena.json"
    ARENA_KEY: str = "arena"
    SIZE_KEY: str = "size"
    SEGMENTS_KEY: str = "segments"
    OBSTACLE_KEY: str = "obstacle"
    SEGMENT_SIZE: float = 0.2
    SIZE: float = 0.9

class Drone:
    """
    Configuration parameters for the drone.

    Attributes:
        A_TOL (float): Absolute tolerance for drone operations.
        WIDTH (float): The drone's width.
        OPERATIONAL_WIDTH (float): The swath width (usually equal to WIDTH) used for sensor coverage.
        MIN_TURNING_RADIUS (float): The minimum turning radius for the drone.
        MAX_DIFF_CURV (float): The maximum differential curvature.
        INITIAL_X (float): The initial X coordinate.
        INITIAL_Y (float): The initial Y coordinate.
        HEIGHT (float): Fleight height (Z coordinate)
    """
    A_TOL: float = 0.2
    WIDTH: float = 0.115
    OPERATIONAL_WIDTH: float = WIDTH  # Defines the swaths width, should be the diameter of the Range Finder sensor spread
    MIN_TURNING_RADIUS: float = 0.05
    MAX_DIFF_CURV: float = 0.25
    INITIAL_X: float = 0.0
    INITIAL_Y: float = 0.0
    HEIGHT: float = 1.0


class Flie:
    """
    Configuration for ROS drone identifiers and related naming.

    Attributes:
        ID (int): The unique identifier for this drone.
        SAFEFLIE_NAME (str): The safeflie name used for drone communication.
        TF_NAME (str): The transform frame name for coordinate transforms.
        NODE_NAME (str): The ROS node name.
        BASE_FRAME (str): The base frame for transformations.
        QOS_PROFILE (int): Quality of Service profile identifier.
    """
    ID: int = 0
    SAFEFLIE_NAME: str = f"safeflie{ID}"
    TF_NAME: str = f"cf{ID}"
    NODE_NAME: str = "tha_flie"
    BASE_FRAME: str = "world"
    QOS_PROFILE: int = 10


class Field:
    """
    Field-related configuration parameters.

    Attributes:
        TARGET (str): Key name for the target.
        TRANSLATION (str): Key name for translation parameters.
        ZRANGE (str): Key name for the z-range.
    """
    TARGET: str = "target"
    TRANSLATION: str = "translation"
    ZRANGE: str = "zrange"


class Topic:
    """
    Communication topic definitions for drone commands.

    Attributes:
        TAKEOFF (str): Topic used to command takeoff.
        LAND (str): Topic used to command landing.
        SEND_TARGET (str): Topic used for sending target coordinates.
    """
    TAKEOFF: str = Flie.SAFEFLIE_NAME + "/takeoff"
    LAND: str = Flie.SAFEFLIE_NAME + "/land"
    SEND_TARGET: str = Flie.SAFEFLIE_NAME + "/send_target"


class Render:
    """
    Configuration for rendering and visualization.

    Attributes:
        OBSTACLE (str): Character representing an obstacle.
        EMPTY (str): Character representing an empty cell.
        ROUTE (str): Character representing a cell in a route.
        DRONE (str): Character representing the drone.
        VISITED (str): Character representing a visited empty cell.
        ANIMATION_FILEPATH (str): File path to the animation script.
        PATH_VISUALIZATION_FILEPATH (str): File path to the path visualization graph.
    """
    OBSTACLE: str = "#"
    EMPTY: str = "."
    ROUTE: str = "O"
    DRONE: str = "v"  # directional drone: "^", ">", "v", "<"
    VISITED: str = "X"
    ANIMATION_FILEPATH: str = "/home/rosrunner/Documents/Flugrobotik/TeamRoboss/Flugrobotik_WS202425/src/roboss/roboss/render/animation.py"
    PATH_VISUALIZATION_FILEPATH: str = "/home/rosrunner/Documents/Flugrobotik/TeamRoboss/Flugrobotik_WS202425/path.png"

    class Color:
        """
        Color code definitions for rendering output.

        Attributes:
            BLACK (int): Code for black.
            RED (int): Code for red.
            GREEN (int): Code for green.
            YELLOW (int): Code for yellow.
            BLUE (int): Code for blue.
            MAGENTA (int): Code for magenta.
            CYAN (int): Code for cyan.
            GREY (int): Code for grey.
            WHITE (int): Code for white.
        """
        BLACK: int = 30
        RED: int = 31
        GREEN: int = 32
        YELLOW: int = 33
        BLUE: int = 34
        MAGENTA: int = 35
        CYAN: int = 36
        GREY: int = 37
        WHITE: int = 38
