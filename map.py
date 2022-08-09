from constants import WIDTH
from drawable import Drawable
from pygame.surface import Surface
from pygame.draw import rect
from pygame.color import Color
from pygame.math import Vector2
from pygame.rect import Rect
from dataclasses import dataclass


@dataclass(slots=True)
class GridElement:
    rect: Rect
    color: Color
    pos: Vector2


class Map(Drawable):
    GRID_WIDTH = 50
    GRID_HEIGHT = 50
    COLOR = Color(126, 0, 0)
    COLOR_COLLIDE = Color(0, 126, 0)

    def __init__(self) -> None:
        super().__init__()
        self.rect_list: list[GridElement] = []
        for x in range(0, WIDTH, self.GRID_WIDTH):
            for y in range(0, WIDTH, self.GRID_WIDTH):
                r = Rect(x, y, self.GRID_WIDTH, self.GRID_HEIGHT)
                pos = Vector2((x + self.GRID_WIDTH) / 2, (y + self.GRID_HEIGHT) / 2)
                self.rect_list.append(GridElement(r, self.COLOR, pos))

    def draw(self, screen: Surface) -> None:
        for r in self.rect_list:
            rect(screen, r.color, r.rect, 1)

    def collide(self, other: Rect):
        for el in self.rect_list:
            if el.rect.colliderect(other):
                el.color = self.COLOR_COLLIDE
                return
