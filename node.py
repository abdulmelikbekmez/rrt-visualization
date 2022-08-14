from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar
from pygame.color import Color
from pygame.math import Vector2
from constants import *
from decorators import rad_to_deg
import numpy as np
from pygame.draw import circle, line
from pygame.surface import Surface


@dataclass(slots=True)
class Node:

    COLOR: ClassVar[Color] = Color(255, 0, 0)
    COLOR_SELECTED: ClassVar[Color] = Color(0, 255, 0)
    RADIUS_SELECTED = 20
    ID: ClassVar[int] = 0

    pos: Vector2
    angle: float  # degree
    reversed: bool
    parent: Node | None = None
    childs: list[Node] = field(default_factory=list)
    color: Color = field(init=False)
    id: int = field(init=False)
    radius: float = 5

    def __post_init__(self):
        self.color = self.COLOR
        self.id = Node.ID
        Node.ID += 1

    def __eq__(self, other: object) -> bool:
        match other:
            case Node():
                return self.id == other.id
            case _:
                return False

    @property
    def direction(self) -> Vector2:
        x = np.cos(np.deg2rad(self.angle))
        y = np.sin(np.deg2rad(self.angle))
        return Vector2(x, y)

    def draw(self, screen: Surface):
        circle(screen, self.color, self.pos, self.radius)
        v = Vector2()
        v.from_polar((10, self.angle))
        line(screen, Color(0, 0, 255), self.pos, self.pos + v, 5)

    @rad_to_deg
    def __get_angle_from_child(self, child: Vector2):
        dif = child - self.pos
        return np.arctan2(dif.y, dif.x)

    def add_child(self, pos: Vector2, reversed: bool) -> Node:
        angle = self.__get_angle_from_child(pos)
        child = Node(pos, angle, reversed, self)
        self.childs.append(child)
        return child

    def set_selected(self):
        self.radius = self.RADIUS_SELECTED
        self.color = self.COLOR_SELECTED


@dataclass(slots=True)
class Connection:
    _from: Node
    length: float
