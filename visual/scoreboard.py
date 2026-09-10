from __future__ import annotations

import pygame


class Scoreboard:
    def __init__(self, font: pygame.font.Font, title: str):
        self.font = font
        self.title = title

    def draw(self, surface: pygame.Surface, x: int, y: int, metrics: dict):
        lines = [
            self.title,
            f"Status: {metrics.get('status', 'running')}",
            f"Time (s): {metrics.get('runtime', 0.0):.4f}",
            f"Cost: {metrics.get('cost', 0.0):.2f}",
            f"Explored: {metrics.get('explored', 0)}",
            f"Path len: {metrics.get('path_len', 0)}",
        ]
        for i, text in enumerate(lines):
            img = self.font.render(text, True, (240, 240, 240))
            surface.blit(img, (x, y + i * 20))
