# pyright: basic
from time import perf_counter, sleep

from loguru import logger


def timeit(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        return_value = func(*args, **kwargs)
        end = perf_counter()
        duration = end - start
        logger.debug(f"Database operation took {duration} seconds")
        return return_value

    return wrapper


@timeit
def a_database_operation() -> None:
    sleep(1)


a_database_operation()
