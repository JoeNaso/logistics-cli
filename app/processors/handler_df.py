"""
Simple utilities for processing flight dataset
"""
import functools
import os
import time

import pandas as pd

from constants import DATA_DIR, ROOT_DIR


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


def get_flight_df() -> pd.DataFrame:
    target = os.path.join(os.sep, ROOT_DIR, DATA_DIR, "input_data_airport_flights.csv")
    return pd.read_csv(target)


def merge_and_clean(
    airports: pd.DataFrame, inbound: pd.DataFrame, outbound: pd.DataFrame
) -> pd.DataFrame:
    """
    Clean up aggregated flight DF for presentation
    """
    # merge 'em and clean up
    airports_inbound = airports.merge(
        inbound, how="left", left_on="IATA Code", right_on="Destination IATA"
    )
    airports_all = airports_inbound.merge(
        outbound, how="left", left_on="IATA Code", right_on="Origin IATA"
    )
    output = airports_all[["Origin IATA", "total_seats_outbound", "total_seats_inbound"]]
    return output


@calc_time
def aggregate_df() -> pd.DataFrame:
    """
    Aggregate inbound and outbound seat data by airport in DataFrame
    """
    flights = get_flight_df()
    # make a clean "total seats" column since data is inconsistent
    flights["total_seats"] = flights[
        ["Fclass Seats", "Bclass Seats", "Eclass Seats"]
    ].sum(axis=1)

    # Get outbound and inbound totals as Series
    outbound = (
        flights.groupby(["Origin IATA"])["total_seats"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"total_seats": "total_seats_outbound"})
    )
    inbound = (
        flights.groupby(["Destination IATA"])["total_seats"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"total_seats": "total_seats_inbound"})
    )

    # get all unique airports (dest or origin)
    # This is used as the spine for the returned data
    airports = pd.DataFrame(
        pd.unique(flights[["Origin IATA", "Destination IATA"]].values.ravel("K"))
    ).rename(columns={0: "IATA Code"})

    final = merge_and_clean(airports, inbound, outbound)
    return final
