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
    RADIUS_SELECTED: ClassVar[int] = 20

    MARGIN_MAX: ClassVar[int] = 75
    MARGIN_MIN: ClassVar[int] = 60
    MAX_ANGLE: ClassVar[int] = 45
    ID: ClassVar[int] = 0

    pos: Vector2
    angle: float  # degree
    reversed: bool
    parent: Node | None = None
    cost: float = 0
    childs: list[Node] = field(default_factory=list)
    color: Color = field(init=False)
    id: int = field(init=False)
    radius: float = 5

    @property
    def direction(self) -> Vector2:
        x = np.cos(np.deg2rad(self.angle))
        y = np.sin(np.deg2rad(self.angle))
        return Vector2(x, y)

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

    @classmethod
    def refactor_length(cls, length: float) -> float:
        if length > cls.MARGIN_MAX:
            return cls.MARGIN_MAX
        elif length < cls.MARGIN_MIN:
            return cls.MARGIN_MIN
        else:
            return length

    def is_in_range(self, point: Vector2) -> bool:
        dir = point - self.pos
        if dir.length() > self.MARGIN_MAX:
            return False
        return abs(self.direction.angle_to(dir)) < self.MAX_ANGLE / 2

    def is_close_enough(self, goal_pos: Vector2):
        return (self.pos - goal_pos).length() < self.MARGIN_MAX

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
        cost = (self.pos - pos).length()
        child = Node(pos, angle, reversed, self, self.cost + cost)
        self.childs.append(child)
        return child

    def set_selected(self):
        self.radius = self.RADIUS_SELECTED
        self.color = self.COLOR_SELECTED
