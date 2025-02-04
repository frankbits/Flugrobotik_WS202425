from adodbapi.ado_consts import directions

from Arena import Arena, Field

from .RoutePlanner import RoutePlanner

DIRECTIONS = {
    'up': (-1, 0),
    'right': (0, 1),
    'down': (1, 0),
    'left': (0, -1)
}

class SpiralRoutePlanner(RoutePlanner):
    def __init__(self, arena: Arena, startPos: tuple):
        self.direction = 0
        self.arena = arena
        self.startPos = startPos

    def plan_route(self):
        """
        Find the fastest full coverage route.
        :return: List of tuples with the route.
        """
        route = []
        n_correct = 1
        current_pos = self.startPos
        self.row = current_pos[0]
        backTrackIndex = 1
        while True:
            route.append(current_pos)
            print('current_pos', current_pos, self.direction)
            self.arena.segments[current_pos[0]][current_pos[1]].visited = True
            current_pos = self.next_pos(current_pos)
            if current_pos is None:
                print('current_pos', current_pos)
                print('backTrackIndex', backTrackIndex)
                # Check if the route is finished
                print('n_correct', n_correct)
                print('self.arena.n_fields', self.arena.n_fields)
                if n_correct >= self.arena.n_fields:
                    break
                # Backtrack until a new direction is found
                if 2*backTrackIndex >= len(route):
                    break
                # Because every backTrack adds an element to the route, the negative index has to be multiplied by 2 (2nd to last, 4th to last, ...)
                current_pos = route.__getitem__(-(2 * backTrackIndex))
                print('current_posBackTrack', current_pos)
                backTrackIndex += 1
            else:
                backTrackIndex = 1
                n_correct += 1
        return route

    def next_pos(self, current_pos: tuple):
        """
        Find the next position in the route.
        :param current_pos: Current position.
        :return: Next position.
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

    def valid_pos(self, pos: tuple):
        """
        Check if the position is valid.
        :param pos: Position to check.
        :return: True if the position is valid.
        """
        if 0 <= pos[0] < self.arena.size and 0 <= pos[1] < self.arena.size:
            if isinstance(self.arena.segments[pos[0]][pos[1]], Field):
                # Check if the field is not visited
                if not self.arena.segments[pos[0]][pos[1]].visited:
                    return True
                return False
        return False