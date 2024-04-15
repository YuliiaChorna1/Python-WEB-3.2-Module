# створення процесів через function

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

def runner(*args, **kwargs):
    sleep(2)

    for i in args:
        logger.debug(f"arg: {i}")

    for key, value in kwargs.items():
        logger.debug(f"kwargs: {key}={value}")

    logger.debug("Finish")


if __name__ == '__main__':
    set_start_method("spawn")

    processes = []

    for i in range(5):
        process = Process(
            target=runner,
            args=(1, 2, 3),
            kwargs={"a": 3, "b": 2}
        )
        
        process.start()
        processes.append(process)

    while any([process.is_alive() for process in processes]): ### option 1
        logger.debug("Waiting...")
        sleep(2)

    # for process in processes: ### option 2
    #     process.join()


    logger.debug("Useful message")
