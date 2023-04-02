import os 
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix

from utils import calc_time, get_flight_df


def get_sparse_matrix_data(airport):
    df = get_flight_df(airport=airport)
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
    return seen_origin, seen_dest


def create_matrix(data: pd.DataFrame) -> coo_matrix:
    """
    Create a sparse matrix, with Origin as rows and Destination as columns
    Coordinates of matrix correspond to the Origin/ Destination pair
    Since airports are string values, 3-letter codes are transposed to a numeric value 
    """
    origin = data['Origin IATA']
    dest = data['Destination IATA']
    encoded_origin, encoded_dest = get_airport_encodings(origin, dest)
    clean_origin = origin.map(encoded_origin)
    clean_dest = dest.map(encoded_dest)
    number_origins = len(origin.unique())
    number_dests = len(dest.unique())
    sparse = coo_matrix((data['total_seats'], 
                         (clean_origin, clean_dest)), 
                         shape=(number_origins, number_dests))
    return sparse


def process_matrix(airport) -> np.ndarray:
    """
    Given an airport code, return the array with to total seats for each corresponding destiation
    Example:
        process_matrix(JFK') -> [[123, 456, 789]]
    Each sublist represents seats leaving JFK and landing at specific destination.
    To find the corresponding destination airport, use `index_to_destination_airport`
    """
    data = get_sparse_matrix_data(airport=airport)
    matrix = create_matrix(data)
    origin, _ = get_airport_encodings(data['Origin IATA'], data['Destination IATA'])
    encoding = origin.get(airport)
    # return matrix.getrow(encoding)
    return matrix.getrow(encoding)


def index_to_destination_airport(idx: int) -> str:
    """
    Given an index, find the destination airport code
    """
    data = get_sparse_matrix_data(airport=None)
    matrix = create_matrix(data)
    _, dest = get_airport_encodings(data['Origin IATA'], data['Destination IATA'])
    swapped = {v:k for k, v in dest.items()}
    return swapped.get(idx, None)
