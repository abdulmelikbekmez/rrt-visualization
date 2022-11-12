from __future__ import annotations
from dataclasses import dataclass, field
from pygame.rect import Rect
from pygame.math import Vector2
from pygame.draw import rect
from pygame.surface import Surface

from node import Node


@dataclass(slots=True)
class Best:
    node: Node | None
    length: float


@dataclass(slots=True, repr=False)
class QuadTree:
    boundary: Rect
    node_list: list[Node] = field(default_factory=list)
    divided_list: list[QuadTree] = field(init=False, default_factory=list)
    max_point: int = 4

    @property
    def node_count(self) -> int:
        l = len(self.node_list)
        for q in self.divided_list:
            l += q.node_count
        return l

    def insert(self, node: Node) -> bool:
        if not self.boundary.collidepoint(node.pos.x, node.pos.y):
            return False

        if len(self.node_list) < self.max_point:
            self.node_list.append(node)
            return True

        if not self.divided_list:
            self.__divide()

        return any(quadtree.insert(node) for quadtree in self.divided_list)

    def get_closest_node(self, point: Vector2) -> Node:
        best = Best(None, self.boundary.width + self.boundary.height)
        new_best = self.__query_point(point, best)

        if new_best.node is None:
            raise Exception("must be handled!!")

        return new_best.node

    def __query_point(self, point: Vector2, best: Best) -> Best:
        x, y = point
        x1, y1 = self.boundary.topleft
        x2, y2 = self.boundary.bottomright
        l = best.length

        if x < x1 - l or x > x2 + l or y < y1 - l or y > y2 + l:
            return best

        for node in self.node_list:
            length = (node.pos - point).length()
            if length < best.length:
                best.length = length
                best.node = node
        for q in self.divided_list:
            best = q.__query_point(point, best)

        return best

    def __divide(self) -> None:
        if self.divided_list:
            raise Exception("already divided")

        w = (self.boundary.w + 8) / 2.0
        h = (self.boundary.h + 8) / 2.0
        self.divided_list.append(
            QuadTree(Rect(self.boundary.left - 2, self.boundary.top - 2, w, h))
        )
        self.divided_list.append(
            QuadTree(Rect(self.boundary.centerx - 2, self.boundary.top - 2, w, h))
        )

        self.divided_list.append(
            QuadTree(Rect(self.boundary.left - 2, self.boundary.centery - 2, w, h))
        )

        self.divided_list.append(
            QuadTree(Rect(self.boundary.centerx - 2, self.boundary.centery - 2, w, h))
        )

    def query_radius(self, radius: float, center: Vector2) -> list[Node]:
        l: list[Node] = []
        left = center.x - radius
        top = center.y - radius
        boundary = Rect(left, top, radius * 2, radius * 2)
        self.__query(boundary, l)

        return [p for p in l if (p.pos - center).length() <= radius]

    def __query(self, boundary: Rect, node_list: list[Node]) -> None:
        if not self.boundary.colliderect(boundary):
            return

        for node in self.node_list:
            if self.boundary.collidepoint(node.pos.x, node.pos.y):
                node_list.append(node)

        for quad in self.divided_list:
            quad.__query(boundary, node_list)

    def draw(self, screen: Surface) -> None:
        rect(screen, (0, 0, 0), self.boundary, 1)
        for q in self.divided_list:
            q.draw(screen)
