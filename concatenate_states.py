#==================================================================#
# CONCATENATE STATES
# Merge state level files for one user set
#
# Cecile Murray
#==================================================================#

import pandas as pd 

PROCESSED = "processed/"
MERGED = "uid/"
BY_STATE = "by-st/"

STATES = ["01", "04", "05", "06", "08"] #, "02", "09", "10", "11", "12", "13",
#  "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27",
#   "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
#   "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]

def main():

    with open(PROCESSED + MERGED + 'u_{:02d}.csv'.format(j), "a") as f:

        for st in STATES:

            df = pd.read_csv(PROCESSED + BY_STATE + 'u_{}_' + st + '.csv')
            df.to_csv(f, index = False, float_format='%.5f', header = False)