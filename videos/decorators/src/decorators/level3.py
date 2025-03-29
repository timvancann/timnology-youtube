# pyright: basic
import functools
from time import perf_counter, perf_counter_ns, sleep

from loguru import logger


def timeit(*, use_nanos: bool = False):
    time_fn = perf_counter_ns if use_nanos else perf_counter

    def func_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time_fn()
            return_value = func(*args, **kwargs)
            end = time_fn()
            duration = end - start
            logger.debug(f"Database operation took {duration}")
            return return_value

        return wrapper

    return func_wrapper


@timeit(use_nanos=True)
def a_database_operation() -> None:
    """An expensive database operation"""
    sleep(1)


a_database_operation()
