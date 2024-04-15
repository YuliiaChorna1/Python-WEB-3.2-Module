# створення процесів через functor

from multiprocessing import Process, set_start_method
import logging
from time import sleep


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(processName)s %(message)s"
)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

class ExecutorClass:

    def __init__(self, seconds):
        self.seconds = seconds

    def __call__(self):
        sleep(self.seconds)
        logger.debug("Wake up!")
        logger.debug(f"args: {self.seconds}")


if __name__ == '__main__':
    set_start_method("spawn")

    for i in range(5):
        process = Process(target=ExecutorClass(i))
        process.start()

    logger.debug("Useful message")

