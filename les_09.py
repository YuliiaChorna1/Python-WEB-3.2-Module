# Pool example

import logging
from multiprocessing import Pool, current_process

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(processName)s %(lineno)s %(message)s")

stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def worker(x):
    logger.debug(f"pid={current_process().pid}, x={x}")
    return x*x


if __name__ == '__main__':
    with Pool(processes=2) as pool:
        logger.debug(pool.map(worker, range(10)))
