from threading import Thread
from time import sleep
from pygame.color import Color
from pygame.math import Vector2
from decorators import synchronized
from drawable import Drawable
from node import Connection, Node
from pygame.surface import Surface
from pygame.draw import circle, line
from constants import *
from random import randint as r
from random import random
import numpy as np


class RRT(Drawable):
    MARGIN_MAX = 75
    MARGIN_MIN = 60
    MAX_ANGLE = 45
    BIAS = 0.05

    def __init__(self, head_pos: Vector2) -> None:
        super().__init__()
        self.head = Node(head_pos, 0, False)
        self.count = 1
        self.started = False
        self.stop = False
        self.finded_node: Node | None = None
        self.last_random_point: Vector2 | None = None

    def __iter__(self):
        self.__iter_list = [self.head]
        return self

    def __next__(self):
        if not self.__iter_list:
            raise StopIteration

        node = self.__iter_list.pop()
        self.__iter_list.extend(node.childs)
        return node

    @synchronized(lock)
    def draw(self, screen: Surface) -> None:
        l = [self.head]
        while l:
            node = l.pop()
            node.draw(screen)
            l.extend(node.childs)
            for child in node.childs:
                line(screen, Color(0, 0, 0), node.pos, child.pos)

        tmp = self.finded_node
        while tmp:
            tmp.draw(screen)
            parent = tmp.parent
            if parent:
                line(screen, (155, 155, 155), tmp.pos, parent.pos, 5)

            tmp = parent

        if self.last_random_point:
            circle(screen, (0, 255, 0), self.last_random_point, 7)

    def __get_closest_node(self, to: Vector2) -> Node:
        return min(
            [Connection(node, (node.pos - to).length()) for node in self],
            key=lambda x: x.length,
        )._from

    def prepare_angle(self, angle: float) -> float:
        if angle > 180:
            return angle - 360
        elif angle < -180:
            return angle + 360
        return angle

    def refactor_angle(self, angle: float, closest_node: Node) -> tuple[float, bool]:
        angle = self.prepare_angle(angle)
        if angle > 180 or angle < -180:
            raise Exception("wrong angle!!")
        x = -1 if angle < 0 else 1
        angle = abs(angle)

        if angle > 90 and not closest_node.reversed:
            angle = max(180 - self.MAX_ANGLE / 2, 180 - angle)
            reversed = True
        else:
            angle = min(self.MAX_ANGLE / 2, angle)
            reversed = False

        return angle * x, reversed

    def refactor_length(self, length: float):
        if length > self.MARGIN_MAX:
            return self.MARGIN_MAX
        elif length < self.MARGIN_MIN:
            return self.MARGIN_MIN
        else:
            return length

    def __get_closest_point_from_node_with_max_angle(
        self, closest_node: Node, random_point: Vector2
    ) -> tuple[Vector2, bool]:
        dir = random_point - closest_node.pos
        dif_angle = closest_node.direction.angle_to(dir)
        dif_angle_refactored, reversed = self.refactor_angle(dif_angle, closest_node)
        length = self.refactor_length(dir.length())
        v = Vector2()
        v.from_polar((length, closest_node.angle + dif_angle_refactored))
        return closest_node.pos + v, reversed

    def generate_random_point(self, goal: Vector2) -> Vector2:
        rand = random()
        if rand < self.BIAS:
            return goal

        return Vector2(r(0, WIDTH), r(0, HEIGHT))

    @synchronized(lock)
    def __create_new_node(self, goal: Vector2) -> bool:
        """
        Creates new node randomly and returns True if new node is not close enough to goal
        """
        random_point = self.generate_random_point(goal)
        self.last_random_point = random_point
        closest_node = self.__get_closest_node(random_point)
        closest_point, reversed = self.__get_closest_point_from_node_with_max_angle(
            closest_node, random_point
        )
        child_node = closest_node.add_child(closest_point, reversed)
        self.count += 1
        if (closest_point - goal).length() > self.MARGIN_MAX:
            return True
        else:
            self.finded_node = child_node
            self.last_random_point = None
            child_node.set_selected()
            return False

    def __runnable(self, goal: Vector2):
        while self.__create_new_node(goal) and not self.stop:
            # sleep(0.0001)
            sleep(0.5)

    def main(self, goal: Vector2):
        self.started = True
        Thread(target=self.__runnable, args=(goal,)).start()

    def reset(self):
        pass
