import csv
import os

from typing import Dict

from constants import ROOT_DIR, DATA_DIR


def get_total_seats(row: Dict) -> int:
    seat_classes = ['Fclass Seats', 'Bclass Seats', 'Eclass Seats']
    return sum(int(v) for k, v in row.items() if k in seat_classes and v != '')


def aggregate_dict() -> Dict:
    """
    Aggregate inbound and outbound seat data by airport in Dictionary
    """
    report = {}

    target = os.path.join(os.sep, ROOT_DIR, DATA_DIR, "input_data_airport_flights.csv")
    with open(target, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            origin = row.get('Origin IATA')
            destination = row.get('Destination IATA')
            # Set origin key in report dict if not present
            if not origin in report:
                report[origin] = {
                    'total_seats_outbound': get_total_seats(row)
                }
            else:
                # Process outbound seats, and increment if 
                # we've seen this airport already
                org = report[origin]
                if not 'total_seats_outbound' in org:
                    org['total_seats_outbound'] = get_total_seats(row)
                else:
                    org['total_seats_outbound'] += get_total_seats(row)
            # Set destination key in report dict if not already present
            if not destination in report:
                report[destination] = {
                    'total_seats_inbound': get_total_seats(row)
                }
            else:
                # Process inbound seats, and increment if 
                # we've seen this airport already
                dest = report[destination]
                if not 'total_seats_inbound' in dest:
                    dest['total_seats_inbound'] = get_total_seats(row)
                else:
                    dest['total_seats_inbound'] += get_total_seats(row)
    return report
            
