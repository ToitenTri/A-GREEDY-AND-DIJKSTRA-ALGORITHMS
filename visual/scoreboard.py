from math import isfinite

import pygame


class Scoreboard:
    def __init__(self, font: pygame.font.Font, title: str):
        self.font = font
        self.title = title

    def draw(self, surface: pygame.Surface, x: int, y: int, metrics: dict):
        status = metrics.get('status', 'running')
        cost = metrics.get('cost', 0.0)
        cost_text = f"{cost:.2f}" if status == 'done' and isfinite(cost) else 'N/A'
        time_text = f"{metrics.get('runtime', 0.0):.6f}" if status != 'running' else '...'
        lines = [
            self.title,
            f"Status: {metrics.get('status', 'running')}",
            f"Search time (s): {time_text}",
            f"Cost: {cost_text}",
            f"Explored: {metrics.get('explored', 0)}",
            f"Path len: {metrics.get('path_len', 0)}",
        ]
        for i, text in enumerate(lines):
            img = self.font.render(text, True, (240, 240, 240))
            surface.blit(img, (x, y + i * 20))
