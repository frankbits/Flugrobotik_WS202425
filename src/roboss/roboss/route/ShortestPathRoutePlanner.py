from ..arena.Arena import Arena, Field

from .RoutePlanner import RoutePlanner

DIRECTIONS = {
    'up': (-1, 0),
    'right': (0, 1),
    'down': (1, 0),
    'left': (0, -1),
    'up-right': (-1, 1),
    'down-right': (1, 1),
    'down-left': (1, -1),
    'up-left': (-1, -1)
}

class ShortestPathRoutePlanner(RoutePlanner):
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
        # start at the start position
        current_pos = self.startPos
        route.append(current_pos)
        self.arena.segments[current_pos[0]][current_pos[1]].visited = True
        # while there are unvisited fields
        n_correct = 1
        while True:
            # get the next position
            next_pos = self.nearest_unvisited(current_pos)
            # if there is no next position, break
            if not next_pos:
                break
            # add the path to the next position to the route
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
            # set the current position to the next position
            current_pos = next_pos
        return route

    def shortest_path(self, current_pos: tuple, target_pos: tuple):
        #find the shortest path between two points
        if current_pos == target_pos:
            return []
        path = []
        new_pos = None
        # check if any of the directions is valid
        while True:
            distance = self.distance(current_pos, target_pos)
            # try ring around the current position with the distance
            for direction in [DIRECTIONS['up'], DIRECTIONS['right'], DIRECTIONS['down'], DIRECTIONS['left']]:
                # get the new position
                try_pos = (current_pos[0] + direction[0],
                           current_pos[1] + direction[1])
                #print('try_pos', try_pos)
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

    # TODO: mischung aus try diagonal und try paths -> trennen
    def nearest_unvisited(self, current_pos: tuple):
        #find the nearest unvisited field
        nearest = None
        distance = 1

        possible_paths = []

        while True:
            directions = [DIRECTIONS['up'], DIRECTIONS['right'], DIRECTIONS['down'], DIRECTIONS['left']]
            directionChanges = [DIRECTIONS['down-right'], DIRECTIONS['down-left'], DIRECTIONS['up-left'], DIRECTIONS['up-right']]
            possible_paths = [(current_pos, 0)]
            for possible_path in possible_paths:
                # try all directions
                for directionIndex, direction in enumerate(directions):
                    # try direction and all fields diagonally between the current direction and the next direction
                    while not direction == directions[(directionIndex+1)%4]:
                        try_pos = (possible_path[0][0] + direction[0], possible_path[0][1] + direction[1])
                        if self.valid_pos(try_pos):
                            print('try_pos', try_pos, self.valid_pos(try_pos))
                            nearest = try_pos
                            break
                        elif self.valid_pos(try_pos) == False:
                            possible_paths.append((try_pos, distance))
                        direction = (direction[0] + directionChanges[directionIndex][0], direction[1] + directionChanges[directionIndex][1])
                    if nearest:
                        break
                if nearest:
                    break
            if nearest or distance > self.arena.size:
                break
            distance += 1
        return nearest



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
        return None

    def distance(self, pos, target_pos):
        """
        Calculate the Manhattan distance between two positions.
        :param pos:
        :param target_pos:
        :return:
        """
        return abs(pos[0] - target_pos[0]) + abs(pos[1] - target_pos[1])