class RoutePlanner:
    def __init__(self, graph, start):
        self.graph = graph
        self.start = start

    def find_route(self):
        route = []
        stack = [[self.start]]
        visited = set()
        while stack:
            path = stack.pop()
            node = path[-1]
            if node == self.end:
                route = path
                break
            if node not in visited:
                visited.add(node)
                for adjacent in self.graph.get(node, []):
                    new_path = list(path)
                    new_path.append(adjacent)
                    stack.append(new_path)
        return route
