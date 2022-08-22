from __future__ import annotations
from dataclasses import dataclass, field
from pygame.math import Vector2
import numpy as np


@dataclass(slots=True)
class Node:
    pos: Vector2
    angle: float
    prev: Node | None = field(default=None)
    childs: list[Node] = field(default_factory=list)

    def add_child(self, pos: Vector2):
        dif = self.pos - pos
        angle = np.arctan2(dif.y, dif.x)
        node = Node(pos, angle, self)
        self.childs.append(node)
