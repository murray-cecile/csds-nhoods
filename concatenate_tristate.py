#=========================================================================#
# CONCATENATE DATA ACROSS JOBS FOR THE TRI-STATE AREA
# Merge all user id files for IL, MN, and WI; drop imprecise
#
# Cecile Murray
#=========================================================================#

import pandas as pd 
import argparse


UID_LIST = [x + y for x in "0123456789abcdef" for y in "0123456789abcdef"]


def main(st_list, uid_list):

  if not uid_list:
    uid_list = UID_LIST

    for st in st_list:

        for j in uid_list:

            print('u_{}/{}.csv.bz2'.format(j, st))
            df = pd.read_csv('u_{}/{}.csv.bz2'.format(j, st), 
                            names = ["uid", "ts", "tract", "lat", "lon", "acc", "hway"],
                            dtype = {'uid': str, 'ts': int, 'tract': str, 'lat': float, 'lon': float, 'acc': int, 'hway': int})
            # print(df.head())
            df.drop(df[df.uid == '0'].index, inplace = True) 
            df.drop(df[df.acc > 500].index, inplace = True)
            # print(df.head())
            df.to_csv('tristate.csv.bz2', mode = 'a', index = False, float_format='%.5f', header = False, compression = 'bz2')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-st", "--st",  nargs='+', help="state fips code")
    parser.add_argument('-uids', "--uids", help="a list of uids", action='append')
    args = parser.parse_args()
    
    main(st_list = args.st, uid_list=args.uids)
