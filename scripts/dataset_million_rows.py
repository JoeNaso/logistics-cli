import random

import pandas as pd


def build_row():
    cols = [
        'Year', 'N6Code', 'OriginAirport', 'DestinationAirport', 'WeightShare', 'Output'
    ]

    yield {}


def build_dataframe() -> bool:
