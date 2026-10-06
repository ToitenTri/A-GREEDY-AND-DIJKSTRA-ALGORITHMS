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


def _neighbors(maze: np.ndarray, node: Coordinate):
    rows, cols = maze.shape
    r, c = node
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] != -1:
            yield (nr, nc)


def _reconstruct(parent: Dict[Coordinate, Coordinate], start: Coordinate, goal: Coordinate) -> List[Coordinate]:
    if goal not in parent and goal != start:
        return []
    path = [goal]
    cur = goal
    while cur != start:
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    return path


def dijkstra_steps(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> Generator[SearchStep, None, SearchResult]:
    """Duyệt Dijkstra theo từng bước.

    Luôn mở rộng ô có chi phí tích lũy g(n) nhỏ nhất và dừng khi
    lấy ô đích ra khỏi hàng đợi ưu tiên.

    Args:
        maze: Ma trận NumPy, -1 là tường, >0 là chi phí đi vào ô.
        start: Tọa độ bắt đầu (row, col).
        goal: Tọa độ đích (row, col).

    Yields:
        SearchStep: Ô vừa được chốt (pop khỏi hàng đợi ưu tiên) và số ô đã duyệt.

    Returns:
        SearchResult: Đường đi, tổng chi phí, số ô đã duyệt, thời gian chạy.
    """
    t0 = time.perf_counter()
    pq: List[Tuple[float, Coordinate]] = [(0.0, start)]
    g_cost: Dict[Coordinate, float] = {start: 0.0}
    parent: Dict[Coordinate, Coordinate] = {}
    visited: Set[Coordinate] = set()

    explored = 0
    while pq:
        current_cost, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        explored += 1
        yield SearchStep(current=current, explored_count=explored)

        if current == goal:
            break

        for nxt in _neighbors(maze, current):
            new_cost = current_cost + float(maze[nxt])
            if new_cost < g_cost.get(nxt, float("inf")):
                g_cost[nxt] = new_cost
                parent[nxt] = current
                heapq.heappush(pq, (new_cost, nxt))

    runtime = time.perf_counter() - t0
    path = _reconstruct(parent, start, goal)
    total_cost = g_cost.get(goal, float("inf")) if path else float("inf")
    return SearchResult(path=path, total_cost=total_cost, explored_nodes=explored, runtime=runtime)


def run_dijkstra(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> SearchResult:
    gen = dijkstra_steps(maze, start, goal)
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
    result = run_dijkstra(maze, (0, 0), (4, 4))
    print("Dijkstra")
    print("Path:", result.path)
    print("Total cost:", result.total_cost)
    print("Explored nodes:", result.explored_nodes)
    print("Runtime (s):", result.runtime)
