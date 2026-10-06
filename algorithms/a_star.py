import heapq
from math import inf, isfinite

import numpy as np

if __package__:
    from .common import Coordinate, SearchGenerator, SearchResult, SearchStep, demo, finish_search, manhattan, neighbors, search_result, timed_search
else:
    from common import Coordinate, SearchGenerator, SearchResult, SearchStep, demo, finish_search, manhattan, neighbors, search_result, timed_search


@timed_search
def astar_steps(
    maze: np.ndarray, start: Coordinate, goal: Coordinate, heuristic_weight: float = 1.0
) -> SearchGenerator:
    """Prioritize g + w*h; w=1 is optimal A*, w>1 is Weighted A*."""
    if not isfinite(heuristic_weight):
        raise ValueError("Heuristic weight must be finite.")
    weight = max(1.0, heuristic_weight)
    h = manhattan(start, goal)
    queue = [(weight * h, h, 0.0, start)]
    distances = {start: 0.0}
    parent = {}
    closed = set()
    explored = 0
    while queue:
        _, _, cost, current = heapq.heappop(queue)
        if current in closed or cost > distances[current]:
            continue
        closed.add(current)
        explored += 1
        yield SearchStep(current, explored)
        if current == goal:
            break
        for nxt in neighbors(maze, current):
            new_cost = cost + float(maze[nxt])
            if new_cost < distances.get(nxt, inf):
                distances[nxt] = new_cost
                parent[nxt] = current
                closed.discard(nxt)  # Reopen a better path, also for Weighted A*.
                h = manhattan(nxt, goal)
                heapq.heappush(queue, (new_cost + weight * h, h, new_cost, nxt))
    return search_result(parent, maze, start, goal, explored)


def run_astar(
    maze: np.ndarray, start: Coordinate, goal: Coordinate, heuristic_weight: float = 1.0
) -> SearchResult:
    return finish_search(astar_steps(maze, start, goal, heuristic_weight))


if __name__ == "__main__":
    demo("A*", run_astar)
