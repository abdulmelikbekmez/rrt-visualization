from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar
from random import randint
from numpy.typing import NDArray
import numpy as np
from node import Node
from pygame.math import Vector2
import matplotlib.pyplot as plt


def normalize_angle(func):

    def wrapper(*args, **kwargs):

        angle = func()

    return wrapper


@dataclass(slots=True)
class Connection:
    from_: Node
    cost: float


@dataclass(slots=True)
class RRT:
    parent: Node
    WIDTH: ClassVar[int] = 512
    HEIGHT: ClassVar[int] = 512
    MARGIN: ClassVar[int] = 100
    MAX_ANGLE: ClassVar[float] = np.pi * 2
    map: NDArray = field(init=False)

    def __post_init__(self):
        self.map = np.ones((self.WIDTH, self.HEIGHT)) * .5

    def __set_map(self, pos: Vector2, val: int = 5):
        self.map[int(pos.x), int(pos.y)] = val

    @classmethod
    def __get_closest_point(cls, from_: Vector2, pos: Vector2) -> Vector2:
        dif = from_ - pos
        if not dif.length() > cls.MARGIN:
            return pos

        dir = dif.normalize()
        return from_ + dir * cls.MARGIN

    def __get_angle(self, dif: Vector2) -> float:
        return np.arctan2(dif.y, dif.x)

    def __get_closest_node(self, pos: Vector2) -> Connection | None:
        tmp = self.parent
        l: list[Connection] = list()
        nodes = [tmp]
        while nodes:
            current = nodes.pop()
            nodes.extend(current.childs)
            dif = pos - current.pos
            dif_angle = self.__get_angle(dif)
            if abs(dif_angle - current.angle) > self.MAX_ANGLE:
                continue
            l.append(Connection(current, dif.length()))

        return min(l, key=lambda x: x.cost) if l else None

    def main(self, goal: Vector2) -> None:
        random_point = Vector2(randint(0, self.WIDTH - 1),
                               randint(0, self.HEIGHT - 1))

        closest_connection = self.__get_closest_node(random_point)
        while not closest_connection:
            random_point = Vector2(randint(0, self.WIDTH - 1),
                                   randint(0, self.HEIGHT - 1))

            closest_connection = self.__get_closest_node(random_point)
        from_ = closest_connection.from_
        closest_point = self.__get_closest_point(from_.pos, random_point)
        from_.add_child(closest_point)
        while (closest_point - goal).length() > self.MARGIN:
            random_point = Vector2(randint(0, self.WIDTH - 1),
                                   randint(0, self.HEIGHT - 1))

            closest_connection = self.__get_closest_node(random_point)
            while not closest_connection:
                random_point = Vector2(randint(0, self.WIDTH - 1),
                                       randint(0, self.HEIGHT - 1))
                closest_connection = self.__get_closest_node(random_point)

            from_ = closest_connection.from_
            closest_point = self.__get_closest_point(from_.pos, random_point)
            from_.add_child(closest_point)

        res: list[Vector2] = [closest_point]
        tmp = from_
        while tmp:
            res.append(tmp.pos)
            tmp = tmp.prev

        for pos in res:
            self.__set_map(pos)

        plt.matshow(self.map)
        plt.show()
