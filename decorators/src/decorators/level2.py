# pyright: basic
from time import perf_counter, perf_counter_ns, sleep

from loguru import logger


def timeit(*, use_nanos: bool = False):
    timer = perf_counter if not use_nanos else perf_counter_ns

    def func_wrapper(func):
        def wrapper(*args, **kwargs):
            start = timer()
            func(*args, **kwargs)
            end = timer()
            duration = end - start
            logger.debug(f"Database operation took {duration}")

        return wrapper

    return func_wrapper


@timeit(use_nanos=True)
def a_database_operation():
    sleep(1)


a_database_operation()
help(a_database_operation)
