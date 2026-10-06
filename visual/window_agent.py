from dataclasses import dataclass, field

import numpy as np
import pygame

from visual.scoreboard import Scoreboard

from algorithms.common import Coordinate, SearchGenerator, manhattan


@dataclass
class AgentPanel:
    name: str
    maze: np.ndarray
    start: Coordinate
    goal: Coordinate
    step_generator: SearchGenerator
    scoreboard: Scoreboard
    panel_rect: pygame.Rect
    cell_size: int = 18
    explored: set[Coordinate] = field(default_factory=set)
    final_path: list[Coordinate] = field(default_factory=list)
    path_cells: set[Coordinate] = field(default_factory=set, init=False)
    done: bool = False
    runtime: float = 0.0
    cost: float = 0.0
    explored_nodes: int = 0
    weight_labels: dict = field(default_factory=dict, init=False, repr=False)
    show_heuristic: bool = False

    def __post_init__(self):
        # Cache labels for both weights and Manhattan distances.
        font = pygame.font.Font(None, max(6, int(self.cell_size * 0.85)))
        available = max(1, self.cell_size - 3)
        rows, cols = self.maze.shape
        max_h = max(self.goal[0], rows - 1 - self.goal[0]) + max(self.goal[1], cols - 1 - self.goal[1])
        values = set(range(max_h + 1)) | {int(weight) for weight in np.unique(self.maze) if weight != -1}
        for weight in values:
            label = font.render(str(int(weight)), True, (20, 20, 20))
            width, height = label.get_size()
            scale = min(1.0, available / width, available / height)
            if scale < 1.0:
                label = pygame.transform.smoothscale(
                    label, (max(1, int(width * scale)), max(1, int(height * scale)))
                )
            self.weight_labels[int(weight)] = label

    def displayed_value(self, row: int, col: int) -> int:
        if self.show_heuristic:
            return manhattan((row, col), self.goal)
        # Starting here costs nothing; other cells show their entry weight.
        if (row, col) == self.start:
            return 0
        return int(self.maze[row, col])

    def cell_at(self, position):
        x = position[0] - self.panel_rect.x
        y = position[1] - self.panel_rect.y
        rows, cols = self.maze.shape
        if 0 <= x < cols * self.cell_size and 0 <= y < rows * self.cell_size:
            return y // self.cell_size, x // self.cell_size
        return None

    def tick(self):
        if self.done:
            return
        try:
            step = next(self.step_generator)
            self.explored.add(step.current)
            self.explored_nodes = step.explored_count
        except StopIteration as finished:
            result = finished.value
            self.final_path = result.path
            self.path_cells = set(result.path)
            self.cost = result.total_cost
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
                if (r, c) in self.path_cells:
                    color = (100, 220, 120)
                if (r, c) == self.start:
                    color = (80, 140, 255)
                if (r, c) == self.goal:
                    color = (255, 90, 90)

                pygame.draw.rect(screen, color, rect)
                if self.maze[r, c] != -1:
                    label = self.weight_labels[self.displayed_value(r, c)]
                    screen.blit(label, label.get_rect(center=rect.center))

        metrics = {
            "status": ("done" if self.final_path else "no path") if self.done else "running",
            "runtime": self.runtime,
            "cost": self.cost,
            "explored": self.explored_nodes,
            "path_len": len(self.final_path),
        }
        self.scoreboard.draw(screen, x0, y0 + grid_h + 8, metrics)
