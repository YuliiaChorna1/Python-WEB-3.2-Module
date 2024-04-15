# Queue example

from multiprocessing import Queue, JoinableQueue, Process
from queue import Queue, Empty
from time import sleep
import logging
import sys


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(processName)s %(lineno)s %(message)s")

stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

q = JoinableQueue()


class Human:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __call__(self) -> str:
        return f"Human: {self.name}"
    

def worker(queue: JoinableQueue):
    logger.debug("Started...")
    
    while True:
        val = None
        try:
            val = queue.get(timeout=4)
        except Empty:
            break
        logger.debug(f"{val()}")

        queue.task_done()

    logger.debug("Exit")
    sys.exit(0)

def hello_world():
    return "Hello world"

def hey_you():
    return "Hey you!"

def whatever():
    return "whatever"


if __name__ == '__main__':
    w1 = Process(target=worker, args=(q, ))
    w2 = Process(target=worker, args=(q, ))

    w1.start()
    w2.start()

    q.put(hello_world)
    sleep(4)
    q.put(Human("Abc"))
    q.put(hey_you)
    q.put(whatever)

    q.join()
    w1.join()
    w2.join()

    print("Finish")
    