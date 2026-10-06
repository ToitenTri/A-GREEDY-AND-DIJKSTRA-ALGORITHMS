from __future__ import annotations

from pathlib import Path
from dataclasses import replace

import pygame

from algorithms.dijkstra import dijkstra_steps
from algorithms.a_star import astar_steps
from algorithms.greedy import greedy_steps
from maze_generator import load_fixed_mazes
from report.plot_results import plot_results
from visual.scoreboard import Scoreboard
from visual.window_agent import AgentPanel

def build_panels(screen_w: int, screen_h: int, maze_data, font, show_heuristic=False):
    maze, start, goal = maze_data.maze, maze_data.start, maze_data.goal

    margin = 12
    panel_w = (screen_w - margin * 4) // 3
    panel_h = screen_h - margin * 2 - 90

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
        panels.append(AgentPanel(name, maze.copy(), start, goal, gen, Scoreboard(font, name), rect, cell_size,
                                 show_heuristic=show_heuristic))
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

    fixed_maps = load_fixed_mazes()
    level_idx = 0
    maze_data = fixed_maps[level_idx][1]
    show_heuristic = False
    panels = build_panels(screen_w, screen_h, maze_data, font)

    error_message = ""
    summary_done = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    show_heuristic = not show_heuristic
                    for panel in panels:
                        panel.show_heuristic = show_heuristic
                    continue
                next_level_idx = level_idx
                if pygame.K_1 <= event.key <= pygame.K_5:
                    next_level_idx = event.key - pygame.K_1
                elif event.key == pygame.K_UP:
                    next_level_idx = min(level_idx + 1, len(fixed_maps) - 1)
                elif event.key == pygame.K_DOWN:
                    next_level_idx = max(level_idx - 1, 0)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    continue
                elif event.key != pygame.K_r:
                    continue
                if next_level_idx == level_idx and event.key in (pygame.K_UP, pygame.K_DOWN):
                    continue
                level_idx = next_level_idx
                maze_data = fixed_maps[level_idx][1]
                panels = build_panels(screen_w, screen_h, maze_data, font, show_heuristic)
                summary_done = False
                error_message = ""
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                cell = next((cell for panel in panels if (cell := panel.cell_at(event.pos)) is not None), None)
                if cell is None:
                    continue
                if maze_data.maze[cell] == -1:
                    error_message = "Choose an open cell, not a wall."
                    continue
                if event.button == 1:
                    maze_data = replace(maze_data, start=cell)
                else:
                    maze_data = replace(maze_data, goal=cell)
                name, _ = fixed_maps[level_idx]
                fixed_maps[level_idx] = (name, maze_data)
                panels = build_panels(screen_w, screen_h, maze_data, font, show_heuristic)
                summary_done = False
                error_message = ""

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

        rows, cols = maze_data.maze.shape
        label_mode = "Heuristic h (Manhattan)" if show_heuristic else "Entry weight (Start=0)"
        level_text = small_font.render(
            f"{fixed_maps[level_idx][0]} | {rows}x{cols} | Start: {maze_data.start} | Goal: {maze_data.goal} | Cell numbers: {label_mode}",
            True,
            (230, 230, 230),
        )
        hint = small_font.render("1-5 / UP/DOWN: map | Left click: start | Right click: goal | H: weight/heuristic | R: replay | ESC: quit", True, (230, 230, 230))
        screen.blit(level_text, (12, screen_h - 56))
        screen.blit(hint, (12, screen_h - 30))
        if error_message:
            error_text = small_font.render(error_message, True, (255, 140, 140))
            screen.blit(error_text, (12, screen_h - 82))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
