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


class RRT(Drawable):
    MARGIN = 50

    def __init__(self, head_pos: Vector2) -> None:
        super().__init__()
        self.head = Node(head_pos, 0)
        self.started = False
        self.stop = False

    @synchronized(lock)
    def draw(self, screen: Surface) -> None:
        l = [self.head]
        while l:
            node = l.pop()
            node.draw(screen)
            # circle(screen, node.color, node.pos, node.radius)
            l.extend(node.childs)
            for child in node.childs:
                line(screen, Color(0, 0, 0), node.pos, child.pos)

    def __get_closest_node(self, to: Vector2) -> Connection:
        l: list[Connection] = list()
        node_list = [self.head]
        while node_list:
            node = node_list.pop()
            l.append(Connection(node, (node.pos - to).length()))
            node_list.extend(node.childs)

        return min(l, key=lambda x: x.length)

    def __get_closest_point_from_node(self, node: Node, point: Vector2) -> Vector2:
        dif = point - node.pos
        if dif.length() <= self.MARGIN:
            return point

        dir = dif.normalize()
        return node.pos + dir * self.MARGIN

    @synchronized(lock)
    def __get_dif(self, goal: Vector2) -> bool:
        random_point = Vector2(r(0, WIDTH), r(0, HEIGHT))
        node = self.__get_closest_node(random_point)
        closest_point = self.__get_closest_point_from_node(
            node._from, random_point)
        child_node = node._from.add_child(closest_point)
        if (closest_point - goal).length() > self.MARGIN:
            return True
        else:
            child_node.set_selected()
            return False

    def __runnable(self, goal: Vector2):
        while self.__get_dif(goal) and not self.stop:
            sleep(0.01)

    def main(self, goal: Vector2):
        self.started = True
        Thread(target=self.__runnable, args=(goal,)).start()

    def reset(self):
        pass
