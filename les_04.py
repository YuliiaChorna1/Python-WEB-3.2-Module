# Shared memory. simple example

from multiprocessing import Process, RLock
from multiprocessing import Value
from time import sleep
import logging
import ctypes
import sys

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(processName)s %(message)s"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

# def worker(val: Value, lock: RLock):
def worker(val):
    logger.debug("Started")

    # with lock:
    with val.get_lock():
        logger.debug("Inside")
        sleep(1)
        val.value += 1
    
    logger.debug("Done")
    sys.exit(0) 
    # imterpretator Pyton по дефолту поверне 0, 
    # якщо треба якийсь інший - використровуй sys.exit()


if __name__ == '__main__':
    lock = RLock()

    value = Value(ctypes.c_float, 0, lock=lock)
    # value = Value(ctypes.c_float, 0)

    pr1 = Process(target=worker, args=(value, ))
    # pr1 = Process(target=worker, args=(value, lock))
    pr1.start()

    pr2 = Process(target=worker, args=(value, ))
    # pr2 = Process(target=worker, args=(value, lock))
    pr2.start()

    pr1.join()
    pr2.join()

    logger.debug(f"{value.value}") # 2.0

