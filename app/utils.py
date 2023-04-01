"""
General use for all handlers
"""
import functools
import os
import time
from pathlib import Path

DATA_DIR = "data"
ROOT_DIR = Path(__file__).absolute().parent.parent


def calc_time(func):
    """
    Decorator to length of processing run times
    """

    @functools.wraps(func)
    def time_wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        minutes, seconds = divmod(end - start, 60)
        print(f"{func.__qualname__}: {minutes} mins, {round(seconds)} seconds")
        return result

    return time_wrapper

def get_data_filepath() -> str:
    return os.path.join(os.sep, ROOT_DIR, DATA_DIR, "input_data_airport_flights.csv")