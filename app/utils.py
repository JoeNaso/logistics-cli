"""
General use for all handlers
"""
import functools
import os
import time
import sys
from pathlib import Path

import pandas as pd

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

def get_flight_df(airport=None) -> pd.DataFrame:
    target = get_data_filepath()
    df = pd.read_csv(target)
    if airport is None:
        return df
    # Check that the airport exists in the data
    missing_from_dest = airport not in df['Destination IATA'].values
    missing_from_origin = airport not in df['Origin IATA'].values
    if (missing_from_dest and missing_from_origin):
        sys.stdout.write(f'Airport code provided not found in data. Provided code: {airport}')
        sys.exit(1)
    
    df = df[(df['Origin IATA'] == airport) | (df['Destination IATA'] == airport)]
    if df.empty:
        sys.stdout.write(f'Airport code provided not found in data. Provided code: {airport}')
        sys.exit(1)
    return df