import numpy as np
import matplotlib.pyplot as plt
import heapq as hq
from time import perf_counter

WIDTH = 32
HEIGHT = 32


def get_dist(x_0, y_0, x_1, y_1):
    return ((x_1 - x_0) ** 2 + (y_1 - y_0) ** 2) ** .5

# def get_dist(x_0, y_0, x_1, y_1):
#     return abs(x_1 - x_0) + abs(y_1 - y_0)


def get_neighbour(map, x, y):
    """
    (x,y) - cost
    """

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            if x+i < 0 or y+j < 0 or x+i > WIDTH - 1 or y+j > HEIGHT - 1:
                continue

            el = map[x+i][y+j]
            cost = el if i*j == 0 else el * 1.414
            yield (x+i, y+j),  cost


def set_neighbour(map, x, y, value):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            map[x+i][y+j] = value


class GridNode:
    def __init__(self, location):
        # type: (tuple[int, int]) -> None
        self.location = location
        self.cost_heruistic = np.inf
        self.cost_dist = np.inf


def dijkstra(map, s_x, s_y, g_x, g_y):
    costs = {(i, j): GridNode((i, j))
             for i in range(WIDTH) for j in range(HEIGHT)}
    prev = {(i, j): None for i in range(WIDTH) for j in range(HEIGHT)}
    costs[(s_x, s_y)].cost_dist = 0
    costs[(s_x, s_y)].cost_heruistic = 0

    visited = set()

    heap = [(0.0, (s_x, s_y))]

    while heap:
        c, (x, y) = hq.heappop(heap)
        node = costs[(x, y)]

        map[x][y] = 4
        #print(f"popped with elements => {c,x,y}")

        if x == g_x and y == g_y:
            #print("arrived !!!")
            break

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for (n_x, n_y), n_cost in get_neighbour(map, x, y):
            # print(f"neighbour {n_x, n_y} cost {n_cost}")
            if (n_x, n_y) in visited:
                continue
            n_node = costs[(n_x, n_y)]

            new_cost = node.cost_dist + n_cost + get_dist(n_x, n_y, g_x, g_y)

            if new_cost < n_node.cost_heruistic:

                n_node.cost_heruistic = new_cost
                n_node.cost_dist = node.cost_dist + n_cost
                prev[(n_x, n_y)] = (x, y)

                hq.heappush(heap, (new_cost, (n_x, n_y)))

    path = []
    current = (g_x, g_y)

    while current != (s_x, s_y):
        path.insert(0, current)
        current = prev[current]

        if current is None:
            #print("not found")
            return None
    else:
        path.insert(0, (s_x, s_y))

    return path


def main():
    map = np.ones((WIDTH, HEIGHT)) * .5

    # for i in range(5, WIDTH-5):
    #     map[i][i] = np.inf
    #     map[i+1][i] = np.inf
    map[0:25, 22] = np.inf
    map[18:32, 26] = np.inf

    # for i in get_neighbour(map, 5,5):
    #    print(i)

    t_start = perf_counter()
    path = dijkstra(map, 1, 1, 30, 30)
    t_finish = perf_counter()

    # for i in get_neighbour(map, 5,5):
    #    print(i)

    for (x, y) in path:
        map[x][y] = 10

    print(f"dif => {t_finish - t_start}")

    plt.matshow(map)
    plt.show()
