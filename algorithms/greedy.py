import heapq

import numpy as np

if __package__:
    from .common import Coordinate, SearchGenerator, SearchResult, SearchStep, demo, finish_search, manhattan, neighbors, search_result, timed_search
else:
    from common import Coordinate, SearchGenerator, SearchResult, SearchStep, demo, finish_search, manhattan, neighbors, search_result, timed_search


@timed_search
def greedy_steps(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> SearchGenerator:
    """Prioritize h alone; the returned cost is the actual path cost."""
    queue = [(manhattan(start, goal), start)]
    parent = {}
    discovered = {start}
    explored = 0
    while queue:
        _, current = heapq.heappop(queue)
        explored += 1
        yield SearchStep(current, explored)
        if current == goal:
            break
        for nxt in neighbors(maze, current):
            if nxt not in discovered:
                discovered.add(nxt)
                parent[nxt] = current
                heapq.heappush(queue, (manhattan(nxt, goal), nxt))
    return search_result(parent, maze, start, goal, explored)


def run_greedy(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> SearchResult:
    return finish_search(greedy_steps(maze, start, goal))


if __name__ == "__main__":
    demo("Greedy", run_greedy)
