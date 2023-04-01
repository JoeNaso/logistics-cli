import random
from pathlib import Path

import numpy as np
import pandas as pd


ROW_COUNT = 1000000000
ROOT_DIR = Path(__file__).absolute().parent


def build_test_dataframe() -> int:
    df = pd.DataFrame()
    df = pd.read_csv(os.path.join(os.sep, ROOT_DIR, 'data', "IATACODES.csv"))['IATA']
    weightShareList = ['<34kg', '>100,000kg', '10,000-20,000kg', '1000-5000kg', '20,000-50,000kg', '34-68kg',
                       '50,000-100,000kg', '5000-10,000kg', '68-1000kg']

    ###Column1: Year.
    years = np.random.choice(range(2000, 2020), size=ROW_COUNT)
    colDF1 = pd.DataFrame(years, columns=['Year'])

    ###Column2: Origin Port.
    codes = np.random.choice(range(20000, 21001), size=ROW_COUNT)
    colDF2 = pd.DataFrame(codes, columns=['N6Code'])

    ###Column3: Origin Port.
    origin = np.random.choice(df, size=ROW_COUNT)
    colDF3 = pd.DataFrame(origin, columns=['OriginAirport'])

    ###Column4: Destination Port.
    dest = np.random.choice(df, size=ROW_COUNT)
    colDF4 = pd.DataFrame(dest, columns=['DestinationAirport'])

    ###Column5: Weight Segment.
    weights = np.random.choice(weightShareList, size=ROW_COUNT)
    colDF5 = pd.DataFrame(weights, columns=['WeightShare'])

    ###Column6: Output.
    output = np.random.choice(range(1000000, 2000001), size=ROW_COUNT)
    colDF6 = pd.DataFrame(output, columns=['Output'])

    testDataFrame = pd.concat([colDF1, colDF2, colDF3, colDF4, colDF5, colDF6], axis=1)
    testDataFrame.to_csv("million_rows_df_refactored.csv", index=False)

    return 200

if __name__ == "__main__":
    test_df_build_result = build_test_dataframe()
   