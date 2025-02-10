from typing import List, Tuple, Optional

from .RoutePlanner import RoutePlanner
from ..arena.Arena import Arena, Field

DIRECTIONS = {'up': (-1, 0), 'right': (0, 1), 'down': (1, 0), 'left': (0, -1), 'up-right': (-1, 1),
              'down-right': (1, 1), 'down-left': (1, -1), 'up-left': (-1, -1)}


class ShortestPathRoutePlanner(RoutePlanner):
    """
    A route planner that calculates the shortest path between unvisited fields in an arena.

    This class inherits from `RoutePlanner` and implements the `plan_route` method to plan the fastest
    full-coverage route by finding the shortest path between unvisited fields.

    Attributes:
        arena : Arena
            The arena that contains the segments to be traversed.
        startPos : tuple[int, int]
            The starting position in the arena.
        direction : int
            An internal variable used for direction tracking (unused in the current implementation).

    Methods:
        plan_route() -> List[Tuple[int, int]]
            Plans the route through the arena, visiting all unvisited fields in the shortest possible way.
        shortest_path(current_pos: tuple[int, int], target_pos: tuple[int, int]) -> List[Tuple[int, int]]
            Calculates the shortest path between two positions using a greedy approach.
        nearest_unvisited(current_pos: tuple[int, int]) -> Optional[Tuple[int, int]]
            Finds the nearest unvisited field from the current position.
        valid_pos(pos: tuple[int, int]) -> Optional[bool]
            Checks if a given position is valid (within arena bounds and unvisited).
        distance(pos: tuple[int, int], target_pos: tuple[int, int]) -> int
            Computes the Manhattan distance between two positions.
    """

    def __init__(self, arena: Arena, start_pos: Tuple[int, int]):
        """
        Initializes the ShortestPathRoutePlanner with the given arena and starting position.

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
        Plans the shortest route covering all unvisited fields in the arena.

        This method uses a greedy approach to find the nearest unvisited field, and calculates the
        shortest path to it. The process continues until all fields are visited.

        Returns:
            List[Tuple[int, int]]
                A list of tuples representing the route to be followed, starting from the initial position.
        """
        route = []
        current_pos = self.startPos
        route.append(current_pos)
        self.arena.segments[current_pos[0]][current_pos[1]].visited = True
        n_correct = 1

        while True:
            next_pos = self.nearest_unvisited(current_pos)
            if not next_pos:
                break
            shortest_path = self.shortest_path(current_pos, next_pos)
            print('shortest_path', shortest_path)
            route.extend(shortest_path)
            print('next_pos', next_pos)
            self.arena.segments[next_pos[0]][next_pos[1]].visited = True
            n_correct += 1
            if n_correct < 10 or n_correct == self.arena.n_fields:
                print('n_correct', n_correct)
                print('self.arena.n_fields', self.arena.n_fields)
                print('route', route)
            if n_correct >= self.arena.n_fields:
                break
            current_pos = next_pos
        return route

    def shortest_path(self, current_pos: Tuple[int, int], target_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Calculates the shortest path between two positions using a greedy approach.

        Parameters:
            current_pos : tuple[int, int]
                The current position in the arena.
            target_pos : tuple[int, int]
                The target position to reach.

        Returns:
            List[Tuple[int, int]]
                A list of tuples representing the shortest path from `current_pos` to `target_pos`.
        """
        if current_pos == target_pos:
            return []

        path = []
        new_pos = None

        # Check if any of the directions is valid
        while True:
            distance = self.distance(current_pos, target_pos)
            # Try ring around the current position with the distance
            for direction in [DIRECTIONS['up'], DIRECTIONS['right'], DIRECTIONS['down'], DIRECTIONS['left']]:
                try_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])

                if try_pos == target_pos:
                    new_pos = try_pos
                    break
                if self.valid_pos(try_pos) in (True, False):
                    new_distance = self.distance(try_pos, target_pos)
                    if new_distance < distance:
                        new_pos = try_pos
                        distance = new_distance
            if new_pos:
                path.append(new_pos)
                current_pos = new_pos
                if new_pos == target_pos:
                    break
            else:
                break
        return path

    def nearest_unvisited(self, current_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Finds the nearest unvisited field from the current position.

        Parameters:
            current_pos : tuple[int, int]
                The current position in the arena.

        Returns:
            Optional[Tuple[int, int]]
                The position of the nearest unvisited field, or `None` if no unvisited fields are found.
        """
        nearest = None
        distance = 1
        possible_paths = []

        while True:
            directions = [DIRECTIONS['up'], DIRECTIONS['right'], DIRECTIONS['down'], DIRECTIONS['left']]
            direction_changes = [DIRECTIONS['down-right'], DIRECTIONS['down-left'], DIRECTIONS['up-left'],
                                DIRECTIONS['up-right']]
            possible_paths = [(current_pos, 0)]
            for possible_path in possible_paths:
                # try all directions
                for direction_index, direction in enumerate(directions):
                    # try direction and all fields diagonally between the current direction and the next direction
                    while not direction == directions[(direction_index + 1) % 4]:
                        try_pos = (possible_path[0][0] + direction[0], possible_path[0][1] + direction[1])
                        if self.valid_pos(try_pos):
                            print('try_pos', try_pos, self.valid_pos(try_pos))
                            nearest = try_pos
                            break
                        elif self.valid_pos(try_pos) == False:
                            possible_paths.append((try_pos, distance))
                        direction = (direction[0] + direction_changes[direction_index][0],
                                     direction[1] + direction_changes[direction_index][1])
                    if nearest:
                        break
                if nearest:
                    break
            if nearest or distance > self.arena.size:
                break
            distance += 1
        return nearest

    def valid_pos(self, pos: Tuple[int, int]) -> Optional[bool]:
        """
        Checks if a given position is valid (within arena bounds and unvisited).

        Parameters:
            pos : tuple[int, int]
                The position to check.

        Returns:
            Optional[bool]
                `True` if the position is valid and unvisited, `False` if invalid or visited, `None` if out of bounds.
        """
        if 0 <= pos[0] < self.arena.size and 0 <= pos[1] < self.arena.size:
            if isinstance(self.arena.segments[pos[0]][pos[1]], Field):
                # Check if the field is not visited
                if not self.arena.segments[pos[0]][pos[1]].visited:
                    return True
                return False
        return None

    def distance(self, pos: Tuple[int, int], target_pos: Tuple[int, int]) -> int:
        """
        Computes the Manhattan distance between two positions.

        Parameters:
            pos : tuple[int, int]
                The first position.
            target_pos : tuple[int, int]
                The second position.

        Returns:
            int
                The Manhattan distance between `pos` and `target_pos`.
        """
        return abs(pos[0] - target_pos[0]) + abs(pos[1] - target_pos[1])
