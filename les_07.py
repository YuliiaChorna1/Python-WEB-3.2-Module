# Pipes example

from multiprocessing import Pipe, Process, current_process
from time import sleep
import logging
import sys


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(processName)s %(message)s")

stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

recipient1, sender1 = Pipe(duplex=False)
recipient2, sender2 = Pipe(duplex=False)


def worker(pipe: Pipe, id: int):
    name = current_process().name
    logger.debug("Started...")

    # pipe = globals()[f"recipient{id}"]

    val = pipe.recv()

    logger.debug(val**2)
    sys.exit(0)

if __name__ == '__main__':
    w1 = Process(target=worker, args=(recipient1, 1))
    w2 = Process(target=worker, args=(recipient2, 2))

    w1.start()
    w2.start()

    sender1.send(8)
    sleep(1)
    sender2.send(16)
