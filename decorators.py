from time import perf_counter
import numpy as np


# def synchronized(lock: RLock):
#     def wrapper(fn):
#         def inner(*args, **kwargs):
#
#             # with lock:
#             #     # print(f"locked {fn.__name__}")
#             #     res = fn(*args, **kwargs)
#             #
#             #     # print(f"released {fn.__name__}")
#             #
#             # return res
#
#             return fn(*args, **kwargs)
#
#         return inner
#
#     return wrapper


def benchmark(fn):
    def wrapper(*args, **kwargs):

        start = perf_counter()
        res = fn(*args, **kwargs)
        finish = perf_counter()
        dif = finish - start

        print(f"{fn.__name__} execution time => {dif:.5f}")
        return res

    return wrapper


def rad_to_deg(fn):
    def wrapper(*args, **kwargs):

        rad = fn(*args, **kwargs)

        return np.rad2deg(rad)

    return wrapper
