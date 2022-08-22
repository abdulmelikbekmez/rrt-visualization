from time import perf_counter
from pygame.math import Vector2
import numpy as np
from numpy.typing import NDArray
from node import Node

from tree import RRT

WIDTH = 1024
HEIGHT = 1024


def set_map(map: NDArray, pos: Vector2, val: int = 5):
    map[int(pos.x), int(pos.y)] = val


def main():
    start = Vector2(2, 4)
    finish = Vector2(500, 300)
    dif = finish - start
    angle = np.arctan2(dif.y, dif.x)
    rrt = RRT(Node(start, angle))
    t_start = perf_counter()
    rrt.main(finish)
    t_finish = perf_counter()
    print(f"time consumed => {t_finish - t_start}")
