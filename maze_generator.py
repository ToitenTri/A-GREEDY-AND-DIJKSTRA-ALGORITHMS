"""Generate weighted mazes shared by all algorithms."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Tuple

import numpy as np

Coordinate = Tuple[int, int]


@dataclass(frozen=True)
class MazeData:
    maze: np.ndarray
    start: Coordinate
    goal: Coordinate


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
        if path_checker(data.maze, data.start, data.goal):
            return data
    raise RuntimeError("Cannot generate solvable maze with current settings.")
