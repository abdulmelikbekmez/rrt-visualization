from threading import RLock
import numpy as np


def synchronized(lock: RLock):
    def wrapper(fn):
        def inner(*args, **kwargs):

            with lock:
                # print(f"locked {fn.__name__}")
                res = fn(*args, **kwargs)

                # print(f"released {fn.__name__}")

            return res

        return inner

    return wrapper


def rad_to_deg(fn):

    def wrapper(*args, **kwargs):

        rad = fn(*args, **kwargs)

        return np.rad2deg(rad)

    return wrapper
