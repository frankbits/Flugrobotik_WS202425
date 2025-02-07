import json
from dataclasses import dataclass
from typing import List

from config import Config


@dataclass
class Segment:
    pass


@dataclass
class Field(Segment):
    height: int = 0
    visited: bool = False


@dataclass
class Obstacle(Segment):
    pass


class Arena:
    size: int
    segments: List[List[Segment]] = []

    def __init__(self, src):
        parsed_data = json.load(open(src))
        self.size = parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SIZE_KEY]
        self.segments = [
            [
                Obstacle() if segment[Config.Arena.OBSTACLE_KEY] else Field() for segment in row
            ] for row in parsed_data[Config.Arena.ARENA_KEY][Config.Arena.SEGMENTS_KEY]
        ]

    def get_mapped_arena(self):
        return list(
            map(
                lambda x:
                list(
                    map(lambda y: Config.Render.OBSTACLE if isinstance(y, Obstacle) else Config.Render.EMPTY, x)
                ),
                self.segments
            )
        )
