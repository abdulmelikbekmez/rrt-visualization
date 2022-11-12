from threading import Thread
from obstacle import Obstacle
from quadtree import QuadTree
from utils import normalize_angle
from pygame.color import Color
from pygame.math import Vector2
from drawable import Drawable
from node import Node
from pygame.surface import Surface
from pygame.draw import circle, line
from pygame.rect import Rect
from constants import *
from random import randint as r
from random import random


class RRT(Drawable):
    MAP_MARGIN = 100
    BIAS = 0.00
    OBSTACLE_LIST: list[Obstacle]

    def __init__(self, head_pos: Vector2) -> None:
        super().__init__()
        self.quad_tree = QuadTree(
            Rect(
                0 - self.MAP_MARGIN,
                0 - self.MAP_MARGIN,
                WIDTH + self.MAP_MARGIN * 2,
                HEIGHT + self.MAP_MARGIN * 2,
            )
        )
        self.head = Node(head_pos, 180, False)
        self.quad_tree.insert(self.head)
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

    def draw(self, screen: Surface) -> None:
        # self.quad_tree.draw(screen)
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
                line(screen, (200, 100, 100), tmp.pos, parent.pos, 7)

            tmp = parent

        if self.last_random_point:
            circle(screen, (0, 255, 0), self.last_random_point, 7)

        if self.finded_node:
            circle(screen, (0, 0, 255), self.finded_node.pos, 5)

    # @benchmark
    # def __tmp(self, to: Vector2) -> Node:
    #     return min([node for node in self], key=lambda node: (node.pos - to).length())

    def __get_closest_node(self, to: Vector2) -> Node:
        # a = self.__tmp(to)
        b = self.quad_tree.get_closest_node(to)
        # if a.pos != b.pos:
        #     raise Exception("must be equal!!!")
        return b

    def refactor_angle(self, angle: float, closest_node: Node) -> tuple[float, bool]:
        angle = normalize_angle(angle)
        x = -1 if angle < 0 else 1
        angle = abs(angle)

        if angle > 90 and not closest_node.reversed:
            angle = max(180 - closest_node.MAX_ANGLE / 2, 180 - angle)
            reversed = True
        else:
            angle = min(closest_node.MAX_ANGLE / 2, angle)
            reversed = False

        return angle * x, reversed

    @staticmethod
    def __generate_random_point_from_ellipse(
        a: float, b: float, angle: float, pos: Vector2
    ) -> Vector2:
        point = Vector2()
        point.from_polar((random() ** 0.5, random() * 360))

        point.x *= a
        point.y *= b
        point = point.rotate(angle)
        point += pos
        if point.x > WIDTH:
            point.x = WIDTH
        elif point.x < 0:
            point.x = 0

        if point.y > HEIGHT:
            point.y = HEIGHT
        elif point.y < 0:
            point.y = 0

        return point

    def __get_closest_point_from_node_with_max_angle(
        self, closest_node: Node, random_point: Vector2
    ) -> tuple[Vector2, bool]:
        direction = random_point - closest_node.pos
        dif_angle = closest_node.direction.angle_to(direction)
        dif_angle_refactored, reversed = self.refactor_angle(dif_angle, closest_node)
        length = Node.refactor_length(direction.length())
        v = Vector2()
        v.from_polar((length, closest_node.angle + dif_angle_refactored))
        return closest_node.pos + v, reversed

    def generate_random_point(self, goal: Vector2) -> Vector2:
        rand = random()
        if rand < self.BIAS:
            return goal

        # informed rrt star feature
        if self.finded_node:
            length = (self.head.pos - self.finded_node.pos).length()
            center = (self.head.pos + self.finded_node.pos) / 2
            dir = self.finded_node.pos - self.head.pos
            angle = Vector2().angle_to(dir)
            x = length / 2
            d = self.finded_node.cost / 2
            a = self.finded_node.cost / 2
            b = (d**2 - x**2) ** 0.5
            new_point = self.__generate_random_point_from_ellipse(a, b, angle, center)
            return new_point

        return Vector2(r(0, WIDTH), r(0, HEIGHT))

    def get_best_parent(self, closest_point: Vector2, current_parent: Node) -> Node:

        l = [
            node
            for node in self.quad_tree.query_radius(Node.NEIGHBOUR_MAX, closest_point)
            if node.is_in_range(closest_point)
        ]

        # l = [node for node in self if node.is_in_range(closest_point)]

        return (
            min(l, key=lambda node: node.cost + (node.pos - closest_point).length())
            if l
            else current_parent
        )

    def rewire(self, possible_parent: Node) -> None:
        neighbours = [
            node
            for node in self.quad_tree.query_radius(
                Node.NEIGHBOUR_MAX, possible_parent.pos
            )
            if possible_parent.can_be_child(node)
        ]

        # neighbours = [node for node in self if possible_parent.can_be_child(node)]

        for neighbour in neighbours:
            cost = (neighbour.pos - possible_parent.pos).length()
            new_cost = possible_parent.cost + cost
            if new_cost < neighbour.cost:
                neighbour.update_parent(possible_parent, new_cost)

    def set_finded_node(self, new_node: Node) -> None:
        if not self.finded_node:
            self.finded_node = new_node
            return

        if new_node.cost < self.finded_node.cost:
            self.finded_node = new_node

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

        while any((obs.collided(closest_point) for obs in self.OBSTACLE_LIST)):
            random_point = self.generate_random_point(goal)
            self.last_random_point = random_point
            closest_node = self.__get_closest_node(random_point)
            closest_point, reversed = self.__get_closest_point_from_node_with_max_angle(
                closest_node, random_point
            )

        parent = self.get_best_parent(closest_point, closest_node)
        child_node = parent.add_child(closest_point, reversed)
        if not self.quad_tree.insert(child_node):
            raise Exception("quad tree insertion error!!!")
        self.rewire(child_node)
        if not child_node.is_close_enough(goal):
            return True
        else:
            self.set_finded_node(child_node)
            self.last_random_point = None
            # child_node.set_selected()
            return False

    def __runnable(self, goal: Vector2) -> None:
        while self.__create_new_node(goal) and not self.stop:
            pass
            # sleep(0.00000001)
            # sleep(0.5)

        iter = 0
        while iter < 10000 and not self.stop:
            self.__create_new_node(goal)
            iter += 1
            # sleep(0.00000001)
            # sleep(0.5)

    def main(self, goal: Vector2) -> None:
        self.started = True
        Thread(target=self.__runnable, args=(goal,)).start()

    def reset(self):
        pass
