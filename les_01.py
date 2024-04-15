# створення процесів через клас 
# У цьому прикладі ми створили п'ять процесів, у трьох з яких виконали функцію example_work,
# а у двох — це клас MyProcess, який наслідується від класу Process. 
# У процесів є код завершення роботи (0 означає успішне завершення роботи у штатному режимі).
# І після завершення роботи атрибут exitcode містить код завершення. 
# В іншому API multiprocessing багато в чому повторює threading.

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

class MyProcess(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name, daemon=daemon)
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        sleep(2)
        logger.debug("Wake up!")
        logger.debug(f"args: {self.args}")


if __name__ == '__main__':
    set_start_method("spawn")
    # set_start_method("forkserver") - doesn't work on Windows, Unix-ish only


    for i in range(5):
        process = MyProcess(args=(f"Count process - {i}",))
        process.start()

    logger.debug("Useful message")
