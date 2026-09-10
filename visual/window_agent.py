from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Set, Tuple

import numpy as np
import pygame

from visual.scoreboard import Scoreboard

Coordinate = Tuple[int, int]


@dataclass
class AgentPanel:
    name: str
    maze: np.ndarray
    start: Coordinate
    goal: Coordinate
    step_generator: object
    scoreboard: Scoreboard
    panel_rect: pygame.Rect
    cell_size: int = 18
    explored: Set[Coordinate] = field(default_factory=set)
    final_path: List[Coordinate] = field(default_factory=list)
    done: bool = False
    started_at: float = field(default_factory=time.perf_counter)
    runtime: float = 0.0
    cost: float = 0.0
    explored_nodes: int = 0

    def tick(self):
        if self.done:
            return
        self.runtime = time.perf_counter() - self.started_at
        try:
            step = next(self.step_generator)
            self.explored.add(step.current)
            self.explored_nodes = step.explored_count
        except StopIteration as finished:
            result = finished.value
            self.final_path = result.path
            self.cost = result.total_cost if result.total_cost != float("inf") else 0.0
            self.explored_nodes = result.explored_nodes
            self.runtime = result.runtime
            self.done = True

    def draw(self, screen: pygame.Surface):
        x0, y0 = self.panel_rect.x, self.panel_rect.y
        pygame.draw.rect(screen, (45, 45, 45), self.panel_rect)

        rows, cols = self.maze.shape
        grid_h = rows * self.cell_size

        for r in range(rows):
            for c in range(cols):
                x = x0 + c * self.cell_size
                y = y0 + r * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size - 1, self.cell_size - 1)

                if self.maze[r, c] == -1:
                    color = (30, 30, 30)
                else:
                    color = (210, 210, 210)
                if (r, c) in self.explored:
                    color = (255, 200, 120)
                if (r, c) in self.final_path:
                    color = (100, 220, 120)
                if (r, c) == self.start:
                    color = (80, 140, 255)
                if (r, c) == self.goal:
                    color = (255, 90, 90)

                pygame.draw.rect(screen, color, rect)

        metrics = {
            "status": "done" if self.done else "running",
            "runtime": self.runtime,
            "cost": self.cost,
            "explored": self.explored_nodes,
            "path_len": len(self.final_path),
        }
        self.scoreboard.draw(screen, x0, y0 + grid_h + 8, metrics)
