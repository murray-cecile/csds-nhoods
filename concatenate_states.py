#=========================================================================#
# CONCATENATE STATES
# Merge state level files for each 2-digit user ID combo, drop imprecise
#
# Cecile Murray
#=========================================================================#

import pandas as pd 
import argparse

PROCESSED = "processed/"


STATES = ["01", "04", "05", "06", "08", "02", "09", "10", "11", "12", "13",
 "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
  "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
  "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]

def main(j):


    with open(PROCESSED + 'u_{:02d}.csv'.format(j), "a") as f:

        for st in STATES:

            df = pd.read_csv(PROCESSED + 'u_{:02d}/' + st + '.csv')
            df.drop(df[df.acc > 500].index, inplace = True)
            df.to_csv(f, index = False, float_format='%.5f', header = False, compression = 'bz2')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--num",  type = int, default = 0, help="A number!")
    args = parser.parse_args()

    main(j = args.num)
