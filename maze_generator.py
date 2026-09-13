from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass
from typing import Tuple

import numpy as np

Coordinate = Tuple[int, int]


@dataclass(frozen=True)
class MazeData:
    maze: np.ndarray
    start: Coordinate
    goal: Coordinate


def _remove_isolated_regions(maze: np.ndarray, start: Coordinate) -> None:
    """Flood-fill from start; any open cell not reached becomes a wall (-1)."""
    rows, cols = maze.shape
    visited = np.zeros((rows, cols), dtype=bool)
    queue = deque([start])
    visited[start] = True

    while queue:
        r, c = queue.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]:
                if maze[nr, nc] != -1:
                    visited[nr, nc] = True
                    queue.append((nr, nc))
    for r in range(rows):
        for c in range(cols):
            if maze[r, c] != -1 and not visited[r, c]:
                maze[r, c] = -1


def generate_weighted_maze(
    rows: int = 25,
    cols: int = 25,
    wall_prob: float = 0.24,
    weight_min: int = 1,
    weight_max: int = 9,
    seed: int | None = None,
) -> MazeData:
    rng = random.Random(seed)
    maze = np.empty((rows, cols), dtype=np.int32)
    for r in range(rows):
        for c in range(cols):
            if rng.random() < wall_prob:
                maze[r, c] = -1
            else:
                maze[r, c] = rng.randint(weight_min, weight_max)

    start = (0, 0)
    goal = (rows - 1, cols - 1)
    maze[start] = weight_min
    maze[goal] = weight_min

    _remove_isolated_regions(maze, start)

    return MazeData(maze=maze, start=start, goal=goal)


def regenerate_until_path(
    path_checker,
    rows: int = 25,
    cols: int = 25,
    wall_prob: float = 0.24,
    seed: int | None = None,
    max_attempts: int = 200,
) -> MazeData:
    base_seed = seed if seed is not None else random.SystemRandom().randint(0, 10_000_000)
    for attempt in range(max_attempts):
        data = generate_weighted_maze(rows, cols, wall_prob, seed=base_seed + attempt)
        if maze_reachable(data.maze, data.goal):
            return data
    raise RuntimeError("Cannot generate solvable maze with current settings.")


def maze_reachable(maze: np.ndarray, cell: Coordinate) -> bool:
    """After _remove_isolated_regions, any surviving open cell is connected to start."""
    return maze[cell] != -1