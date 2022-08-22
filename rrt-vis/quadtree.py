from __future__ import annotations
from dataclasses import dataclass, field
from pygame.rect import Rect
from pygame.math import Vector2
from pygame.draw import rect
from pygame.surface import Surface

from node import Node


@dataclass(slots=True, repr=False)
class QuadTree:
    boundary: Rect
    node_list: list[Node] = field(default_factory=list)
    divided_list: list[QuadTree] = field(init=False, default_factory=list)
    max_point: int = 4

    def insert(self, node: Node) -> bool:
        if not self.boundary.collidepoint(node.pos.x, node.pos.y):
            return False

        if len(self.node_list) < self.max_point:
            self.node_list.append(node)
            return True

        if not self.divided_list:
            self.divide()

        return any(quadtree.insert(node) for quadtree in self.divided_list)

    def get_closest_node(self, point: Vector2):
        parent = self
        l = [parent]

        while any(
            [i.boundary.collidepoint(point.x, point.y) for i in parent.divided_list]
        ):
            pass

    def divide(self) -> None:
        if self.divided_list:
            raise Exception("already divided")

        w = self.boundary.w / 2
        h = self.boundary.h / 2
        self.divided_list.append(
            QuadTree(Rect(self.boundary.left, self.boundary.top, w, h))
        )
        self.divided_list.append(
            QuadTree(Rect(self.boundary.centerx, self.boundary.top, w, h))
        )

        self.divided_list.append(
            QuadTree(Rect(self.boundary.left, self.boundary.centery, w, h))
        )

        self.divided_list.append(
            QuadTree(Rect(self.boundary.centerx, self.boundary.centery, w, h))
        )

    def query(self, boundary: Rect) -> list[Node]:
        l = []
        self._query(boundary, l)
        return l

    def query_radius(self, radius: float, center: Vector2) -> list[Node]:
        l: list[Node] = []
        left = center.x - radius
        top = center.y - radius
        boundary = Rect(left, top, radius * 2, radius * 2)
        self._query(boundary, l)

        return [p for p in l if (p.pos - center).length() <= radius]

    def _query(self, boundary: Rect, node_list: list[Node]) -> None:
        if not self.boundary.colliderect(boundary):
            return

        for node in self.node_list:
            if self.boundary.collidepoint(node.pos.x, node.pos.y):
                node_list.append(node)

        [quad._query(boundary, node_list) for quad in self.divided_list]

    def draw(self, screen: Surface):
        rect(screen, (0, 0, 0), self.boundary, 1)
        [q.draw(screen) for q in self.divided_list]
