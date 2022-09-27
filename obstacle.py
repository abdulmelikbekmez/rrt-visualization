from drawable import Drawable
from pygame.surface import Surface
from pygame.draw import rect
from pygame.rect import Rect
from pygame.math import Vector2


class Obstacle(Drawable):
    def __init__(self, center: Vector2, width: float = 50) -> None:
        super().__init__()
        self.rect = Rect(center.x - width / 2, center.y - width / 2, width, width)

    def draw(self, screen: Surface) -> None:
        rect(screen, (0, 0, 0), self.rect)

    def collided(self, point: Vector2):
        return self.rect.collidepoint(point.x, point.y)
