from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar
from pygame.color import Color
from pygame.math import Vector2
from constants import *


@dataclass(slots=True)
class Node:

    COLOR: ClassVar[Color] = Color(255, 0, 0)
    COLOR_SELECTED: ClassVar[Color] = Color(0, 255, 0)
    RADIUS_SELECTED = 20

    pos: Vector2
    parent: Node | None = None
    childs: list[Node] = field(default_factory=list)
    color: Color = field(init=False)
    radius: float = 5

    def __post_init__(self):
        self.color = self.COLOR

    def add_child(self, pos: Vector2):
        child = Node(pos, self)
        self.childs.append(child)

    def set_selected(self):
        self.radius = self.RADIUS_SELECTED
        self.color = self.COLOR_SELECTED


@dataclass(slots=True)
class Connection:
    _from: Node
    length: float
