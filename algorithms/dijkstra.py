import heapq
from math import inf

import numpy as np

if __package__:
    from .common import Coordinate, SearchGenerator, SearchResult, SearchStep, demo, finish_search, neighbors, search_result, timed_search
else:
    from common import Coordinate, SearchGenerator, SearchResult, SearchStep, demo, finish_search, neighbors, search_result, timed_search


@timed_search
def dijkstra_steps(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> SearchGenerator:
    queue = [(0.0, start)]
    distances = {start: 0.0}
    parent = {}
    visited = set()
    while queue:
        cost, current = heapq.heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        yield SearchStep(current, len(visited))
        if current == goal:
            break
        for nxt in neighbors(maze, current):
            new_cost = cost + float(maze[nxt])
            if new_cost < distances.get(nxt, inf):
                distances[nxt] = new_cost
                parent[nxt] = current
                heapq.heappush(queue, (new_cost, nxt))
    return search_result(parent, maze, start, goal, len(visited))


def run_dijkstra(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> SearchResult:
    return finish_search(dijkstra_steps(maze, start, goal))


if __name__ == "__main__":
    demo("Dijkstra", run_dijkstra)
