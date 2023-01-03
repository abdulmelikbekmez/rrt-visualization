from __future__ import annotations
from drawable import Drawable
from pygame.surface import Surface
from pygame.draw import rect
from pygame.rect import Rect
from pygame.math import Vector2
from random import randint as rint


class Obstacle(Drawable):
    def __init__(self, center: Vector2, width: float = 50) -> None:
        super().__init__()
        self.rect = Rect(center.x - width / 2, center.y - width / 2, width, width)

    @classmethod
    def random(cls, width: int, height: int) -> Obstacle:
        return Obstacle(Vector2(rint(0, width), rint(0, height)))

    def draw(self, screen: Surface) -> None:
        rect(screen, (0, 0, 0), self.rect)

    def collided(self, point: Vector2) -> bool:
        return self.rect.collidepoint(point.x, point.y)
