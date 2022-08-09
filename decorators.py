from threading import RLock


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
