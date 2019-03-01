#=========================================================================#
# CONCATENATE STATES
# Merge state level files for each 2-digit user ID combo, drop imprecise
#
# Cecile Murray
#=========================================================================#

import pandas as pd 
import argparse

PROCESSED = "processed/"


# STATES = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
#  "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
#   "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
#   "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]

STATES = ['06', '11', '17', '18', '48']

def main(j):

  for st in STATES:

    print(PROCESSED + 'u_{}_{}.csv.bz2'.format(j, st))
    df = pd.read_csv(PROCESSED + 'u_{}_{}.csv.bz2'.format(j, st), 
                    names = ["uid", "ts", "tract", "lat", "lon", "acc", "hway"],
                    dtype = {'uid': str, 'ts': int, 'tract': str, 'lat': float, 'lon': float, 'acc': int, 'hway': int})
    # print(df.head())
    df.drop(df[df.acc > 500].index, inplace = True)
    # print(df.head())
    df.to_csv(PROCESSED + 'u_{}.csv.bz2'.format(j), mode = 'a', index = False, float_format='%.5f', header = False, compression = 'bz2')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--uid",  type = str, default = "00", help="Two-digit user id")
    args = parser.parse_args()

    main(j = args.uid)
