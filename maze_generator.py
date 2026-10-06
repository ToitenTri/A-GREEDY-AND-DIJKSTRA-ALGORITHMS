"""Load the five fixed, connected weighted maps."""

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from algorithms.common import Coordinate, neighbors, validate_maze


@dataclass(frozen=True)
class MazeData:
    maze: np.ndarray
    start: Coordinate
    goal: Coordinate


def load_fixed_mazes() -> list[tuple[str, MazeData]]:
    records = json.loads(Path(__file__).with_name("maze_generator.json").read_text(encoding="utf-8"))
    if not isinstance(records, list) or len(records) != 5:
        raise ValueError("Expected exactly five fixed maps.")
    maps = []
    for record in records:
        raw = np.asarray(record["maze"])
        if not np.issubdtype(raw.dtype, np.integer):
            raise ValueError("Fixed map weights must be integers.")
        start, goal = tuple(record["start"]), tuple(record["goal"])
        validate_maze(raw, start, goal)
        seen = {start}
        pending = [start]
        while pending:
            for cell in neighbors(raw, pending.pop()):
                if cell not in seen:
                    seen.add(cell)
                    pending.append(cell)
        if len(seen) != np.count_nonzero(raw != -1):
            raise ValueError("Every open cell must connect to the start.")
        maps.append((record["name"], MazeData(raw, start, goal)))
    return maps
