#==================================================================#
# CHECK UID-ST CSV
# Check if csv was created, and if not, create an empty file to pass back
#
# Cecile Murray
#==================================================================#

import os 
import argparse
import pandas as pd

def main(j, st):

    if os.path.isfile('u_{}_{}.csv.bz2'.format(j, st)):
        return
    
    else:

        df = pd.DataFrame(index=range(0,1), columns=["advertising_id", "timestamp", "geoid", "latitude", "longitude", "accuracy", "hway"])
        df = df.fillna(0) # with 0s rather than NaNs
        df.to_csv('u_{}_{}.csv.bz2'.format(j, st), mode = "a", compression = 'bz2',
                 index = False, float_format='%.5f', header = False)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--uid",  type = str, default = "01", help="Two-digit user id")
    parser.add_argument("-st", "--state", type = str, default = "11", help="State FIPS code")
    args = parser.parse_args()

    main(j = args.uid, st = args.state)