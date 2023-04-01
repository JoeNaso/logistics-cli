import os 
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy.spare import coo_matrix

from utils import calc_time, get_data_filepath


def get_sparse_matrix_data():
    target = get_data_filepath()
    df = pd.read_csv(target)
    seats = ['Fclass Seats', 'Bclass Seats', 'Eclass Seats']
    df['total_seats'] = df[seats].sum(axis=1)
    return df

def get_airport_encodings(
        origin_series: pd.Series, dest_series: pd.Series
    ) -> Tuple[Dict, Dict]:
    """
    Given two series, map them to numeric values in order to 
    generate coordinates for use in matrix
    """
    seen_origin = {}
    i = 0
    for val in origin_series:
        if val not in seen_origin:
            seen_origin[val] = i 
            i += 1

    seen_dest = {}
    j = 0
    for val in dest_series:
        if val not in seen_dest:
            seen_dest[val] = j
            j += 1
    return origin_series.map(seen_origin), dest_series.map(seen_dest)
    

def create_matrix():
    """
    Create a sparse matrix, with Origin as rows and Destination as columns
    Coordinates of matrix correspond to the Origin/ Destination pair
    Since airports are string values, 3-letter codes are transposed to a numeric value 
    """
    data = get_sparse_matrix_data()
    origin = data['Origin IATA']
    dest = data['Destination IATA']
    encoded_origin, encoded_dest = get_airport_encodings(origin, dest)
    number_origins = len(origin.unique())
    number_dests = len(dest.unique())
    sparse = coo_matrix((data['total_seats'], 
                         (encoded_origin, encoded_dest)), 
                         shape=(number_origins, number_dests))
    return sparse


def process_matrix(airport_code) -> np.ndarray:
    """
    Given an airport code, return the array with to total seats for each corresponding destiation
    Example:
        process_matrix(JFK') -> [[123, 456, 789]]
    Each sublist represents seats leaving JFK and landing at specific destination.
    To find the corresponding destination airport, use `index_to_destination_airport`
    """
    matrix = create_matrix()
    origin, _ = get_airport_encodings()
    encoding = origin.get(airport_code)
    return matrix.getrow(encoding)


def index_to_destination_airport(idx: int) -> str:
    """
    Given an index, find the destination airport code
    """
    _, dest = get_airport_encodings()
    swapped = {v:k for k, v in dest.items()}
    return swapped.get(idx, None)
