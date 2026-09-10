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


def greedy_steps(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> Generator[SearchStep, None, SearchResult]:
    """Duyệt Greedy Best-First Search theo từng bước để phục vụ animation.

    Greedy chỉ dùng heuristic h(n) để ưu tiên ô gần đích hơn,
    không cộng thêm chi phí thực g(n) khi chọn nút kế tiếp.
    """
    t0 = time.perf_counter()
    pq: List[Tuple[float, Coordinate]] = [(_h(start, goal), start)]
    parent: Dict[Coordinate, Coordinate] = {}
    visited: Set[Coordinate] = set()

    explored = 0
    while pq:
        _, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        explored += 1
        yield SearchStep(current=current, explored_count=explored)

        if current == goal:
            break

        for nxt in _neighbors(maze, current):
            if nxt not in visited:
                if nxt not in parent:
                    parent[nxt] = current
                heapq.heappush(pq, (_h(nxt, goal), nxt))

    runtime = time.perf_counter() - t0
    path = _reconstruct(parent, start, goal)
    total_cost = float(sum(maze[p] for p in path[1:])) if path else float("inf")
    return SearchResult(path=path, total_cost=total_cost, explored_nodes=explored, runtime=runtime)


def run_greedy(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> SearchResult:
    """Chạy Greedy đến khi kết thúc và trả về kết quả cuối."""
    gen = greedy_steps(maze, start, goal)
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
    result = run_greedy(maze, (0, 0), (4, 4))
    print("Greedy")
    print("Path:", result.path)
    print("Total cost:", result.total_cost)
    print("Explored nodes:", result.explored_nodes)
    print("Runtime (s):", result.runtime)
