from time import perf_counter, sleep

from loguru import logger


def a_database_operation():
    start = perf_counter()
    sleep(1)
    end = perf_counter()
    duration = end - start
    logger.debug(f"Database operation took {duration} seconds")


a_database_operation()
