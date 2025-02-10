from typing import List, Tuple, Optional

from .RoutePlanner import RoutePlanner
from ..arena.Arena import Arena, Field

DIRECTIONS = {'up': (-1, 0), 'right': (0, 1), 'down': (1, 0), 'left': (0, -1)}


class SpiralRoutePlanner(RoutePlanner):
    """
    A route planner that calculates a spiral path for full coverage of the arena.

    This class inherits from `RoutePlanner` and implements the `plan_route` method to plan the route
    in a spiral pattern, covering the arena in layers. It backtracks when it encounters obstacles or the
    boundary of the arena.

    Attributes:
        arena : Arena
            The arena that contains the segments to be traversed.
        startPos : tuple[int, int]
            The starting position in the arena.
        direction : int
            An internal variable used to track the current movement direction (0: up, 1: right, 2: down, 3: left).
        row : int
            The current row of the position (used in backtracking).
        startPos : tuple[int, int]
            The starting position.

    Methods:
        plan_route() -> List[Tuple[int, int]]
            Plans the spiral route starting from the initial position and covering all fields.
        next_pos(current_pos: tuple[int, int]) -> Optional[Tuple[int, int]]
            Determines the next position in the route based on the current direction.
        valid_pos(pos: tuple[int, int]) -> bool
            Checks if a given position is valid (within arena bounds and unvisited).
    """

    def __init__(self, arena: Arena, start_pos: Tuple[int, int]):
        """
        Initializes the SpiralRoutePlanner with the given arena and starting position.

        Parameters:
            arena : Arena
                The arena to be used for route planning.
            start_pos : tuple[int, int]
                The starting position in the arena.
        """
        self.direction = 0
        self.arena = arena
        self.startPos = start_pos

    def plan_route(self) -> List[Tuple[int, int]]:
        """
        Plans the spiral route that covers all the unvisited fields in the arena.

        The method starts from the initial position and spirals outwards. If the route encounters a boundary
        or an obstacle, it backtracks and continues until all fields are visited.

        Returns:
            List[Tuple[int, int]]
                A list of tuples representing the route to be followed, starting from the initial position.
        """
        route = []
        n_correct = 1
        current_pos = self.startPos
        self.row = current_pos[0]
        back_track_index = 1
        while True:
            route.append(current_pos)
            print('current_pos', current_pos, self.direction)
            self.arena.segments[current_pos[0]][current_pos[1]].visited = True
            current_pos = self.next_pos(current_pos)
            if current_pos is None:
                print('current_pos', current_pos)
                print('back_track_index', back_track_index)
                # Check if the route is finished
                print('n_correct', n_correct)
                print('self.arena.n_fields', self.arena.n_fields)
                if n_correct >= self.arena.n_fields:
                    break
                # Backtrack until a new direction is found
                if 2 * back_track_index >= len(route):
                    break
                # Because every backTrack adds an element to the route, the negative index has to be multiplied by 2 (2nd to last, 4th to last, ...)
                current_pos = route.__getitem__(-(2 * back_track_index))
                print('current_posBackTrack', current_pos)
                back_track_index += 1
            else:
                back_track_index = 1
                n_correct += 1
        return route

    def next_pos(self, current_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Determines the next position in the route based on the current direction.

        The direction alternates between up, right, down, and left, changing direction when boundaries or
        obstacles are encountered.

        Parameters:
            current_pos : tuple[int, int]
                The current position in the arena.

        Returns:
            Optional[Tuple[int, int]]
                The next position to move to, or `None` if no valid next position exists.
        """
        new_pos = None
        if self.direction == 0:
            directions = [DIRECTIONS['up'], DIRECTIONS['right'], DIRECTIONS['down'], DIRECTIONS['left']]
            for direction in directions:
                new_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if new_pos[1] == self.arena.size - 1:
                    self.direction = (self.direction + 1) % 4
                if self.valid_pos(new_pos):
                    break
        if self.direction == 1:
            directions = [DIRECTIONS['right'], DIRECTIONS['down'], DIRECTIONS['left'], DIRECTIONS['up']]
            for direction in directions:
                new_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if new_pos[0] == self.arena.size - 1:
                    self.direction = (self.direction + 1) % 4
                if self.valid_pos(new_pos):
                    break
        if self.direction == 2:
            directions = [DIRECTIONS['down'], DIRECTIONS['left'], DIRECTIONS['up'], DIRECTIONS['right']]
            for direction in directions:
                new_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if new_pos[1] == 0:
                    self.direction = (self.direction + 1) % 4
                if self.valid_pos(new_pos):
                    break
        if self.direction == 3:
            directions = [DIRECTIONS['left'], DIRECTIONS['up'], DIRECTIONS['right'], DIRECTIONS['down']]
            for direction in directions:
                new_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if new_pos[0] == 0:
                    self.direction = (self.direction + 1) % 4
                if self.valid_pos(new_pos):
                    break
        if self.valid_pos(new_pos):
            return new_pos

    def valid_pos(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if the given position is valid (within arena bounds and unvisited).

        Parameters:
            pos : tuple[int, int]
                The position to check.

        Returns:
            bool
                `True` if the position is valid and unvisited, `False` if invalid or visited.
        """
        if 0 <= pos[0] < self.arena.size and 0 <= pos[1] < self.arena.size:
            if isinstance(self.arena.segments[pos[0]][pos[1]], Field):
                # Check if the field is not visited
                if not self.arena.segments[pos[0]][pos[1]].visited:
                    return True
                return False
        return False
