# Shared memory. Advanced example

from multiprocessing import Process, RLock
from multiprocessing.sharedctypes import Value, Array
import ctypes
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(processName)s %(message)s")

stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


class Point(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_double),
        ('y', ctypes.c_double)
    ]


def modify(num: Value, string: Array, arr: Array):
    logger.debug("Started")
    logger.debug(f"Change num: {num.value}")

    with num.get_lock():
        num.value **= 2

    logger.debug(f"to num: {num.value}")

    for i in range(len(string)):
        string[i] = string[i].upper()

    # logger.debug(string)

    with string.get_lock():
        string.value = string.value.upper()

    with arr.get_lock():
        for a in arr:
            a.x **= 2
            a.y **= 2

    logger.debug("Done")


if __name__ == '__main__':
    lock = RLock()

    number = Value(ctypes.c_double, 1.5, lock=lock)
    string = Array(ctypes.c_char, b"hello world", lock=lock)
    array = Array(Point, [(1, -6), (-5, 2), (2, 9)], lock=lock)

    # string = [i for i in "hello world"]

    p = Process(target=modify, args=(number, string, array))
    p2 = Process(target=modify, args=(number, string, array))
    p.start()
    p2.start()

    p.join()
    p2.join()

    logger.debug(f"{number.value}")
    logger.debug(f"{string.value}")
    # logger.debug(f"{string}")
    logger.debug(f"{[(arr.x, arr.y) for arr in array]}")
