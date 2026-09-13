from __future__ import annotations

import heapq
import time
from dataclasses import dataclass
from typing import Dict, Generator, List, Set, Tuple

import numpy as np

Coordinate = Tuple[int, int]


@dataclass
class SearchStep:
    current: Coordinate
    explored_count: int


@dataclass
class SearchResult:
    path: List[Coordinate]
    total_cost: float
    explored_nodes: int
    runtime: float


def _h(a: Coordinate, b: Coordinate) -> float:
    """Heuristic Manhattan giữa hai ô trên lưới 4 hướng."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _neighbors(maze: np.ndarray, node: Coordinate):
    """Sinh các ô láng giềng hợp lệ (không phải tường, trong biên)."""
    rows, cols = maze.shape
    r, c = node
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] != -1:
            yield (nr, nc)


def _reconstruct(parent: Dict[Coordinate, Coordinate], start: Coordinate, goal: Coordinate) -> List[Coordinate]:
    """Khôi phục đường đi từ goal về start bằng bảng parent."""
    if goal not in parent and goal != start:
        return []
    path = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def astar_steps(
    maze: np.ndarray, start: Coordinate, goal: Coordinate, heuristic_weight: float = 2.0
) -> Generator[SearchStep, None, SearchResult]:
    """Duyệt A* theo từng bước.

    A* chọn ô có f(n) = g(n) + w*h(n):
    - g(n): chi phí thực từ start tới n
    - h(n): heuristic Manhattan từ n tới goal
    - w: hệ số heuristic
    """
    t0 = time.perf_counter()
    w = max(1.0, heuristic_weight)
    start_h = _h(start, goal)
    pq: List[Tuple[float, float, float, Coordinate]] = [(start_h, start_h, 0.0, start)]
    g_cost: Dict[Coordinate, float] = {start: 0.0}
    parent: Dict[Coordinate, Coordinate] = {}
    closed_set: Set[Coordinate] = set()
    open_best_f: Dict[Coordinate, float] = {start: start_h}

    explored = 0
    while pq:
        f_cur, _, cur_g, current = heapq.heappop(pq)
        if current in closed_set:
            continue
        if f_cur > open_best_f.get(current, float("inf")):
            continue

        closed_set.add(current)
        explored += 1
        yield SearchStep(current=current, explored_count=explored)

        if current == goal:
            break

        for nxt in _neighbors(maze, current):
            ng = cur_g + float(maze[nxt])
            if nxt in closed_set and ng >= g_cost.get(nxt, float("inf")):
                continue
            if ng < g_cost.get(nxt, float("inf")):
                g_cost[nxt] = ng
                parent[nxt] = current
                h = _h(nxt, goal)
                f = ng + w * h
                open_best_f[nxt] = f
                heapq.heappush(pq, (f, h, ng, nxt))

    runtime = time.perf_counter() - t0
    path = _reconstruct(parent, start, goal)
    total_cost = g_cost.get(goal, float("inf")) if path else float("inf")
    return SearchResult(path=path, total_cost=total_cost, explored_nodes=explored, runtime=runtime)


def run_astar(
    maze: np.ndarray, start: Coordinate, goal: Coordinate, heuristic_weight: float = 2.0
) -> SearchResult:
    gen = astar_steps(maze, start, goal, heuristic_weight=heuristic_weight)
    while True:
        try:
            next(gen)
        except StopIteration as done:
            return done.value


if __name__ == "__main__":
    maze = np.array([
        [1, 2, 2, -1, 1],
        [1, -1, 3, -1, 2],
        [1, 1, 1, 1, 3],
        [-1, -1, 2, -1, 2],
        [1, 1, 1, 1, 1],
    ], dtype=np.int32)
    result = run_astar(maze, (0, 0), (4, 4))
    print("A*")
    print("Path:", result.path)
    print("Total cost:", result.total_cost)
    print("Explored nodes:", result.explored_nodes)
    print("Runtime (s):", result.runtime)
