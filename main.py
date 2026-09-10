from __future__ import annotations

from pathlib import Path

import pygame

from algorithms.Dijkstra import dijkstra_steps, run_dijkstra
from algorithms.a_star import astar_steps
from algorithms.greedy import greedy_steps
from maze_generator import regenerate_until_path
from report.plot_results import plot_results
from visual.scoreboard import Scoreboard
from visual.window_agent import AgentPanel

LEVELS = [
    {"name": "Level 1 (De)", "rows": 20, "cols": 20, "wall_prob": 0.14},
    {"name": "Level 2", "rows": 24, "cols": 24, "wall_prob": 0.18},
    {"name": "Level 3", "rows": 28, "cols": 28, "wall_prob": 0.22},
    {"name": "Level 4", "rows": 32, "cols": 32, "wall_prob": 0.26},
    {"name": "Level 5 (Kho)", "rows": 36, "cols": 36, "wall_prob": 0.30},
]


def _has_path(maze, start, goal) -> bool:
    return bool(run_dijkstra(maze, start, goal).path)


def build_panels(screen_w: int, screen_h: int, maze_data, font):
    maze, start, goal = maze_data.maze, maze_data.start, maze_data.goal

    margin = 12
    panel_w = (screen_w - margin * 4) // 3
    panel_h = screen_h - margin * 2

    rows, cols = maze.shape
    info_h = 130
    inner_pad = 10
    cell_size = max(6, min((panel_w - inner_pad * 2) // cols, (panel_h - info_h - inner_pad * 2) // rows))

    algos = [
        ("Dijkstra", dijkstra_steps(maze.copy(), start, goal)),
        ("A*", astar_steps(maze.copy(), start, goal)),
        ("Greedy", greedy_steps(maze.copy(), start, goal)),
    ]

    panels = []
    for i, (name, gen) in enumerate(algos):
        x = margin + i * (panel_w + margin)
        rect = pygame.Rect(x, margin, panel_w, panel_h)
        panels.append(AgentPanel(name, maze.copy(), start, goal, gen, Scoreboard(font, name), rect, cell_size))
    return panels


def main():
    pygame.init()
    pygame.display.set_caption("Maze Comparison: Dijkstra / A* / Greedy")

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_w, screen_h))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20)
    small_font = pygame.font.SysFont("consolas", 18)

    level_idx = 0
    seed = 42
    cfg = LEVELS[level_idx]
    maze_data = regenerate_until_path(
        _has_path, rows=cfg["rows"], cols=cfg["cols"], wall_prob=cfg["wall_prob"], seed=seed
    )
    panels = build_panels(screen_w, screen_h, maze_data, font)

    summary_done = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    seed += 1
                    cfg = LEVELS[level_idx]
                    maze_data = regenerate_until_path(
                        _has_path, rows=cfg["rows"], cols=cfg["cols"], wall_prob=cfg["wall_prob"], seed=seed
                    )
                    panels = build_panels(screen_w, screen_h, maze_data, font)
                    summary_done = False
                elif event.key == pygame.K_f:
                    cfg = LEVELS[level_idx]
                    maze_data = regenerate_until_path(
                        _has_path, rows=cfg["rows"], cols=cfg["cols"], wall_prob=cfg["wall_prob"], seed=42
                    )
                    panels = build_panels(screen_w, screen_h, maze_data, font)
                    summary_done = False
                elif event.key == pygame.K_UP:
                    level_idx = min(level_idx + 1, len(LEVELS) - 1)
                    cfg = LEVELS[level_idx]
                    maze_data = regenerate_until_path(
                        _has_path, rows=cfg["rows"], cols=cfg["cols"], wall_prob=cfg["wall_prob"], seed=seed
                    )
                    panels = build_panels(screen_w, screen_h, maze_data, font)
                    summary_done = False
                elif event.key == pygame.K_DOWN:
                    level_idx = max(level_idx - 1, 0)
                    cfg = LEVELS[level_idx]
                    maze_data = regenerate_until_path(
                        _has_path, rows=cfg["rows"], cols=cfg["cols"], wall_prob=cfg["wall_prob"], seed=seed
                    )
                    panels = build_panels(screen_w, screen_h, maze_data, font)
                    summary_done = False

        screen.fill((20, 20, 20))
        for p in panels:
            p.tick()
            p.draw(screen)

        if all(p.done for p in panels) and not summary_done:
            results = {
                p.name: {
                    "runtime": p.runtime,
                    "cost": p.cost,
                    "explored": p.explored_nodes,
                    "path_len": len(p.final_path),
                }
                for p in panels
            }
            plot_results(results, output_path=str(Path(__file__).parent / "report" / "comparison.png"))
            summary_done = True

        cfg = LEVELS[level_idx]
        level_text = small_font.render(
            f"{cfg['name']} | size={cfg['rows']}x{cfg['cols']} | wall_prob={cfg['wall_prob']:.2f}",
            True,
            (230, 230, 230),
        )
        hint = small_font.render("R: random | F: fixed(seed=42) | UP/DOWN: level", True, (230, 230, 230))
        screen.blit(level_text, (12, screen_h - 56))
        screen.blit(hint, (12, screen_h - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
