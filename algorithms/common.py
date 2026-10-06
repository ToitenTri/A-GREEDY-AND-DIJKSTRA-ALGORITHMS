from collections.abc import Generator
from dataclasses import dataclass
from functools import wraps
from math import inf
from time import perf_counter

import numpy as np

type Coordinate = tuple[int, int]


@dataclass
class SearchStep:
    current: Coordinate
    explored_count: int


@dataclass
class SearchResult:
    path: list[Coordinate]
    total_cost: float
    explored_nodes: int
    runtime: float = 0.0


type SearchGenerator = Generator[SearchStep, None, SearchResult]


def validate_maze(maze: np.ndarray, start: Coordinate, goal: Coordinate) -> None:
    """Require a nonempty weighted grid and two open, in-bounds endpoints."""
    if maze.ndim != 2 or not maze.size:
        raise ValueError("Maze must be a nonempty 2D array.")
    if not np.issubdtype(maze.dtype, np.number) or np.iscomplexobj(maze):
        raise ValueError("Maze weights must be real numbers.")
    if not np.all(np.isfinite(maze) & ((maze == -1) | (maze >= 1))):
        raise ValueError("Cells must be walls (-1) or finite weights >= 1.")
    rows, cols = maze.shape
    for cell in (start, goal):
        if len(cell) != 2 or not all(isinstance(v, (int, np.integer)) for v in cell):
            raise ValueError("Endpoints must contain two integer coordinates.")
        r, c = cell
        if not (0 <= r < rows and 0 <= c < cols) or maze[r, c] == -1:
            raise ValueError("Endpoints must be open cells inside the maze.")


def neighbors(maze: np.ndarray, node: Coordinate):
    rows, cols = maze.shape
    r, c = node
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] != -1:
            yield nr, nc


def manhattan(a: Coordinate, b: Coordinate) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct(parent: dict[Coordinate, Coordinate], start: Coordinate, goal: Coordinate) -> list[Coordinate]:
    if goal not in parent and goal != start:
        return []
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return path[::-1]


def search_result(parent, maze, start, goal, explored) -> SearchResult:
    path = reconstruct(parent, start, goal)
    cost = sum(float(maze[cell]) for cell in path[1:]) if path else inf
    return SearchResult(path, cost, explored)


def timed_search(search):
    """Time only work inside next(), excluding animation waits and rendering."""
    @wraps(search)
    def steps(maze, start, goal, *args, **kwargs):
        elapsed = 0.0
        t0 = perf_counter()
        validate_maze(maze, start, goal)
        generator = search(maze, start, goal, *args, **kwargs)
        elapsed += perf_counter() - t0
        while True:
            t0 = perf_counter()
            try:
                step = next(generator)
            except StopIteration as done:
                done.value.runtime = elapsed + perf_counter() - t0
                return done.value
            elapsed += perf_counter() - t0
            yield step
    return steps


def finish_search(generator: SearchGenerator) -> SearchResult:
    while True:
        try:
            next(generator)
        except StopIteration as done:
            return done.value


def demo(name, run):
    maze = np.array([
        [1, 2, 2, -1, 1],
        [1, -1, 3, -1, 2],
        [1, 1, 1, 1, 3],
        [-1, -1, 2, -1, 2],
        [1, 1, 1, 1, 1],
    ], dtype=np.int32)
    result = run(maze, (0, 0), (4, 4))
    print(name)
    print("Path:", result.path)
    print("Total cost:", result.total_cost)
    print("Explored nodes:", result.explored_nodes)
    print("Runtime (s):", result.runtime)
