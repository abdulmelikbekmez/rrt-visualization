from threading import Thread
from time import sleep
from pygame.color import Color
from pygame.math import Vector2
from decorators import synchronized
from drawable import Drawable
from node import Connection, Node
from pygame.surface import Surface
from pygame.draw import line
from constants import *
from random import randint as r
from random import random
import numpy as np


class RRT(Drawable):
    MARGIN_MAX = 75
    MARGIN_MIN = 60
    MAX_ANGLE = 30
    BIAS = .5

    def __init__(self, head_pos: Vector2) -> None:
        super().__init__()
        self.head = Node(head_pos, 0)
        self.count = 1
        self.started = False
        self.stop = False

    @synchronized(lock)
    def draw(self, screen: Surface) -> None:
        l = [self.head]
        while l:
            node = l.pop()
            node.draw(screen)
            l.extend(node.childs)
            for child in node.childs:
                line(screen, Color(0, 0, 0), node.pos, child.pos)

    def __get_closest_node(self, to: Vector2) -> Node:
        l: list[Connection] = list()
        node_list = [self.head]
        while node_list:
            node = node_list.pop()
            l.append(Connection(node, (node.pos - to).length()))
            node_list.extend(node.childs)

        return min(l, key=lambda x: x.length)._from

    def __get_closest_point_from_node(self, node: Node, point: Vector2) -> Vector2:
        dif = point - node.pos
        if dif.length() <= self.MARGIN_MAX:
            return point

        dir = dif.normalize()
        return node.pos + dir * self.MARGIN_MAX

    def refactor_angle(self, angle: float):
        x = -1 if angle < 0 else 1
        angle = abs(angle)
        angle = min(self.MAX_ANGLE / 2, angle)
        return angle * x

    def refactor_length(self, length: float):
        if length > self.MARGIN_MAX:
            return self.MARGIN_MAX
        elif length < self.MARGIN_MIN:
            return self.MARGIN_MIN
        else:
            return length

    def __get_closest_point_from_node_with_max_angle(self, node: Node, point: Vector2) -> Vector2:
        dif = point - node.pos
        tmp_angle = np.rad2deg(np.arctan2(dif.y, dif.x))
        dif_angle = node.angle - tmp_angle
        dif_angle = self.refactor_angle(dif_angle)
        length = self.refactor_length(dif.length())
        v = Vector2()
        v.from_polar((length, node.angle - dif_angle))
        return node.pos + v

    def generate_random_point(self, goal: Vector2) -> Vector2:
        rand = random()
        if rand < self.BIAS:
            return goal

        return Vector2(r(0, WIDTH), r(0, HEIGHT))

    @synchronized(lock)
    def __create_new_node(self, goal: Vector2) -> bool:
        """
        Creates new node randomly and returns True if new node is close enough to goal 
        """
        random_point = self.generate_random_point(goal)
        node = self.__get_closest_node(random_point)
        closest_point = self.__get_closest_point_from_node_with_max_angle(
            node, random_point)
        child_node = node.add_child(closest_point)
        self.count += 1
        if (closest_point - goal).length() > self.MARGIN_MAX:
            return True
        else:
            child_node.set_selected()
            return False

    def __runnable(self, goal: Vector2):
        while self.__create_new_node(goal) and not self.stop:
            sleep(0.01)

    def main(self, goal: Vector2):
        self.started = True
        Thread(target=self.__runnable, args=(goal,)).start()

    def reset(self):
        pass
